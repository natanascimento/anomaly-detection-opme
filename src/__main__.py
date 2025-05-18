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
        description="Padronizar a nomenclatura dos itens extraídos da nota fiscal.",
        expected_output="Lista de itens com nomes padronizados.",
        agent=normalizer_agent,
        context=[invoice_reader_task]
    )

    classifier_task = Task(
        description="Classificar os itens como OPME, Medicamento ou Material de Consumo.",
        expected_output="Lista de itens classificados por categoria.",
        agent=classifier_agent,
        context=[normalizer_task],
        async_execution=True
    )

    anomaly_task = Task(
        description="Verificar a lista de produtos e identificar anomalias ou inconsistências.",
        expected_output="Lista de produtos com potenciais anomalias identificadas.",
        agent=anomaly_detector_agent,
        context=[normalizer_task],
        async_execution=True
    )

    summary_task = Task(
        description="Crie um resumo consolidado do processo de análise da nota fiscal, incluindo os produtos extraídos, os nomes normalizados, suas classificações e quaisquer anomalias detectadas.",
        expected_output="Resumo textual amigável contendo todos os dados relevantes do processo para exibição ao usuário.",
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

    print(run_crew(pdf_path=path.join(settings.app.DATA_PATH, "sample_invoice.pdf")))
    
    end = datetime.now()
    print("Elapsed Time: ", end - start)