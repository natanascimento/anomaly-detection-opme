from crewai import Agent

from agents.invoice_reader.tools import pdf_reader


class InvoiceReaderAgent(Agent):

    def __init__(self):
        super().__init__(
            role='Invoice Reader Agent',
            goal=(
                'Ler arquivos PDF de notas fiscais, extrair informações relevantes como '
                'produtos, valores, CNPJs, datas e retornar os dados'
                'padronizada definida previamente pelo sistema.'
            ),
            backstory=(
                'Você é um agente especializado em leitura e interpretação de documentos fiscais em PDF. '
                'Sua função é identificar e extrair campos estruturados das notas fiscais, como descrição dos '
                'produtos, código do produto, quantidade, valor unitário, valor total, CNPJ do emitente, CNPJ '
                'do destinatário, data de emissão e número da nota. Após a leitura, os dados devem ser retornados '
                'de forma padronizada e facilmente interpretável por outros sistemas.'
            ),
            tools=[pdf_reader],
            verbose=True
        )
