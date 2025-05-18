from crewai import Agent

from agents.invoice_reader.tools import pdf_reader


class InvoiceReaderAgent(Agent):

    def __init__(self):
        super().__init__(
            role='Simple Invoice Reader Agent',
            goal='Ler e processar notas fiscais em PDF',
            backstory='Agente especializado em leitura de documentos PDF.',
            tools=[pdf_reader],
            verbose=True
        )