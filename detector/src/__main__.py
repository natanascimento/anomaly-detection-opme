from datetime import datetime
from os import path

from crewai import Crew, Task

from core.config import settings
from agents import InvoiceReaderAgent, AnomalyDetectorAgent, NormalizerAgent, ClassifierAgent, SummaryAgent


invoice_reader_agent = InvoiceReaderAgent()
anomaly_detector_agent = AnomalyDetectorAgent()
normalizer_agent = NormalizerAgent()
classifier_agent = ClassifierAgent()
summary_agent = SummaryAgent()

def create_tasks(pdf_path):

    invoice_reader_task = Task(
        description=f"Ler o arquivo o arquivo pdf e extrair os itens da nota fiscal presente no diretório {pdf_path}.",
        expected_output="Texto bruto contendo os produtos descritos na nota fiscal.",
        agent=invoice_reader_agent
    )

    normalizer_task = Task(
        description="Identificar nomenclaturas incorretas e padronizar a nomenclatura dos itens extraídos da nota fiscal.",
        expected_output="Lista de itens com nomes errado e ao lado os nomes padronizados.",
        agent=normalizer_agent,
        context=[invoice_reader_task]
    )

    classifier_task = Task(
        description="Classificar os itens como OPME, Medicamento ou Material de Consumo.",
        expected_output="Lista de itens classificados por categoria definidas.",
        agent=classifier_agent,
        context=[normalizer_task],
        async_execution=True
    )

    anomaly_task = Task(
        description=(
            "Analisar a lista de produtos normalizados da nota fiscal para identificar anomalias como: "
            "preços abusivos ou acima da média de mercado, variações injustificadas entre itens similares, "
            "quantidades incompatíveis com a prática hospitalar, subclassificações conflitantes, ou descrições que não condizem com a categoria. "
            "Utilizar referências como bases históricas, tabelas públicas (ex: BPS/ANVISA), regras regulatórias e lógica clínica para embasar os achados. "
            "Priorizar a detecção de padrões suspeitos que possam indicar sobrepreço, erros sistemáticos ou inconformidades críticas."
        ),
        expected_output=(
            "Lista estruturada de produtos com potenciais anomalias, contendo para cada item:\n"
            "- ID do produto;\n"
            "- Tipo(s) de anomalia(s) detectada(s) (ex: preço abusivo, quantidade atípica, classificação inconsistente);\n"
            "- Justificativa ou evidência (ex: comparação com preço de referência);\n"
            "- Grau de severidade (leve, moderado, crítico);\n"
            "- Sugestão de ação (ex: revisar com fornecedor, reclassificar, encaminhar para auditoria especializada)."
        ),
        agent=anomaly_detector_agent,
        context=[normalizer_task],
        async_execution=True
    )

    summary_task = Task(
        description=(
            "Gerar um resumo consolidado e estruturado de toda a análise realizada sobre a nota fiscal. "
            "O resumo deve incluir: (1) os produtos extraídos, (2) os nomes após normalização, (3) a classificação de cada item "
            "(como OPME, Medicamento ou Consumo), (4) quaisquer anomalias ou inconsistências detectadas e (5) correções ou ajustes sugeridos. "
            "Apresente os dados de forma clara, ordenada e amigável ao usuário, destacando os pontos críticos e possíveis ações recomendadas."
        ),
        expected_output=(
            "Resumo textual estruturado com seções bem definidas, incluindo: \n"
            "- Lista dos produtos processados com nome normalizado, classificação e status de conformidade;\n"
            "- Anomalias detectadas por produto (com descrição breve e impacto potencial);\n"
            "- Correções realizadas ou sugeridas (ex: ajustes de nomenclatura);\n"
            "- Observações gerais e recomendações finais para o usuário.\n"
            "O conteúdo deve ser direto, legível e pronto para visualização em interface ou relatório final."
        ),
        agent=summary_agent,
        context=[invoice_reader_task, normalizer_task, classifier_task, anomaly_task]
    )

    return [invoice_reader_task, normalizer_task, classifier_task, anomaly_task, summary_task]

def run_crew(pdf_path):

    tasks = create_tasks(pdf_path=pdf_path)

    crew = Crew(
        agents=[
            invoice_reader_agent,
            normalizer_agent,
            classifier_agent,
            anomaly_detector_agent,
            summary_agent
        ],
        tasks=tasks,
        verbose=True
    )

    result = crew.kickoff()

    return result

if __name__ == "__main__":
    start = datetime.now()

    print(run_crew(pdf_path=path.join(settings.app.DATA_PATH, "hospital_nf_mock.pdf")))
    
    end = datetime.now()
    print("Elapsed Time: ", end - start)