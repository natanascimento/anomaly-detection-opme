import chromadb
from chromadb.utils import embedding_functions
import os
import pandas as pd

MAX_BATCH_SIZE = 5000
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = os.getenv("CHROMA_PORT", "8000")
COLLECTION_NAME = "anomaly_detector_products_database"
DOCUMENTS_PATH = "../datalake/bronze/DADOS_ABERTOS_MEDICAMENTOS.csv"
TEXT_COLUMN_FOR_EMBEDDING = "NOME_PRODUTO"
METADATA_COLUMNS = ["TIPO_PRODUTO", "CATEGORIA_REGULATORIA", "CLASSE_TERAPEUTICA", "PRINCIPIO_ATIVO"]
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_and_prepare_documents_from_csv(file_path, text_column, metadata_columns):
    """
    Carrega o conteúdo de um arquivo CSV, usando uma coluna para o texto principal
    e outras colunas para os metadados.
    """
    df = pd.read_csv(file_path, encoding='cp1252', sep=';')

    documents_for_embedding = []
    metadatas = []

    for index, row in df.iterrows():
        main_text = str(row[text_column]) if text_column in row and pd.notna(row[text_column]) else ""
        documents_for_embedding.append(main_text.strip())

        doc_metadata = {}
        for col in metadata_columns:
            if col in row and pd.notna(row[col]):
                doc_metadata[col] = str(row[col])
            else:
                doc_metadata[col] = "N/A"
        metadatas.append(doc_metadata)

    return documents_for_embedding, metadatas, df.columns.tolist()

def chunk_text(text, chunk_size=200, chunk_overlap=20):
    """
    Divide o texto em chunks com sobreposição.
    Para produção, considere usar bibliotecas como Langchain Text Splitters.
    """
    if not text.strip():
        return [""]

    chunks = []
    words = text.split()
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            # Ajuste para evitar divisão por zero se word for vazio
            overlap_words_count = min(len(current_chunk), int(chunk_overlap / (len(word) + 1) if word else 1))
            current_chunk = current_chunk[-overlap_words_count:]
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def main():
    print(f"Conectando ao ChromaDB em http://{CHROMA_HOST}:{CHROMA_PORT}...")
    try:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        client.heartbeat()
        print("Conexão com o ChromaDB estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao ChromaDB: {e}")
        print("Certifique-se de que o ChromaDB está rodando via `docker compose up -d`.")
        return

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )

    print(f"Criando/Obtendo a coleção '{COLLECTION_NAME}'...")
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )
    print(f"Coleção '{COLLECTION_NAME}' pronta.")

    print(f"Carregando documentos de '{DOCUMENTS_PATH}'...")
    try:
        documents_to_embed, metadatas_from_csv, all_csv_columns = load_and_prepare_documents_from_csv(
            DOCUMENTS_PATH, TEXT_COLUMN_FOR_EMBEDDING, METADATA_COLUMNS
        )
        print(f"Colunas detectadas no CSV: {', '.join(all_csv_columns)}")
        print(f"Texto para embedding será gerado da coluna: {TEXT_COLUMN_FOR_EMBEDDING}")
        print(f"Metadados serão gerados das colunas: {', '.join(METADATA_COLUMNS)}")
        print(f"Carregadas {len(documents_to_embed)} linhas do CSV para processamento.")

    except Exception as e:
        print(f"Erro ao carregar ou preparar o CSV: {e}")
        return

    all_final_chunks = []
    all_final_ids = []
    all_final_metadatas = []
    chunk_counter_global = 0

    for i, doc_content in enumerate(documents_to_embed):
        chunks_for_doc = chunk_text(doc_content)
        doc_metadata = metadatas_from_csv[i]

        for chunk in chunks_for_doc:
            all_final_chunks.append(chunk)
            current_id = f"doc_{i}_chunk_{chunk_counter_global}"
            all_final_ids.append(current_id)
            all_final_metadatas.append(doc_metadata)
            chunk_counter_global += 1

    print(f"Total de {len(all_final_chunks)} chunks gerados a partir do CSV.")

    print(f"Adicionando chunks e embeddings ao ChromaDB em lotes de {MAX_BATCH_SIZE}...")
    try:
        if not all_final_chunks:
            print("Nenhum chunk gerado para adicionar ao ChromaDB.")
            return

        total_chunks = len(all_final_chunks)
        for i in range(0, total_chunks, MAX_BATCH_SIZE):
            batch_chunks = all_final_chunks[i : i + MAX_BATCH_SIZE]
            batch_ids = all_final_ids[i : i + MAX_BATCH_SIZE]
            batch_metadatas = all_final_metadatas[i : i + MAX_BATCH_SIZE]

            print(f"Adicionando lote {i // MAX_BATCH_SIZE + 1} de {len(batch_chunks)} chunks (IDs de {i} a {i + len(batch_chunks) - 1})...")

            collection.add(
                documents=batch_chunks,
                ids=batch_ids,
                metadatas=batch_metadatas
            )
            print(f"Lote {i // MAX_BATCH_SIZE + 1} adicionado.")

        print(f"Total de {total_chunks} documentos (chunks) adicionados à coleção '{COLLECTION_NAME}'.")

    except Exception as e:
        print(f"Erro ao adicionar documentos: {e}")
        return

    print("\nRealizando uma busca de exemplo com metadados:")
    query_text = "medicamento para dor de cabeça"
    results = collection.query(
        query_texts=[query_text],
        n_results=2,
        include=['documents', 'distances', 'metadatas']
    )
    print(f"Consulta: '{query_text}'")
    print("Resultados:")
    if results and results['documents']:
        for i, doc in enumerate(results['documents'][0]):
            print(f"  {i+1}. Documento: '{doc}'")
            print(f"     ID: {results['ids'][0][i]}")
            print(f"     Distância: {results['distances'][0][i]:.4f}")
            print(f"     Metadados: {results['metadatas'][0][i]}")
    else:
        print("Nenhum resultado encontrado para a consulta.")

    print("\nRealizando uma busca de exemplo:")
    filtered_results = collection.query(
        query_texts=["medicamento para gripe"],
        n_results=2,
        include=['documents', 'distances', 'metadatas']
    )
    print(f"Consulta com filtro: 'medicamento para gripe'")
    print("Resultados Filtrados:")
    if filtered_results and filtered_results['documents']:
        for i, doc in enumerate(filtered_results['documents'][0]):
            print(f"  {i+1}. Documento: '{doc}'")
            print(f"     ID: {filtered_results['ids'][0][i]}")
            print(f"     Distância: {filtered_results['distances'][0][i]:.4f}")
            print(f"     Metadados: {filtered_results['metadatas'][0][i]}")
    else:
        print("Nenhum resultado encontrado para a consulta com filtro.")


if __name__ == "__main__":
    main()