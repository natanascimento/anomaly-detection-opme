from crewai import Crew, Task
from agents.invoice_reader import InvoiceReaderAgent
from agents.anomaly_detector import AnomalyDetectorAgent
from agents.normalizer import NormalizerAgent
from agents.classifier import ClassifierAgent
from agents.summary import SummaryAgent
from dotenv import load_dotenv

load_dotenv()

invoice_reader_agent = InvoiceReaderAgent()
anomaly_detector_agent = AnomalyDetectorAgent()
normalizer_agent = NormalizerAgent()
classifier_agent = ClassifierAgent()
summary_agent = SummaryAgent()

invoice_reader_task = Task(
    description="Ler e extrair os itens da nota fiscal enviada pelo usuário.",
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


crew = Crew(
    agents=[
        invoice_reader_agent,
        normalizer_agent,
        classifier_agent,
        anomaly_detector_agent,
        summary_agent
    ],
    tasks=[
        invoice_reader_task,
        normalizer_task,
        classifier_task,
        anomaly_task,
        summary_task
    ],
    verbose=True
)

def main():
    final_result = crew.kickoff()

    print(final_result)

if __name__ == "__main__":
    main()
