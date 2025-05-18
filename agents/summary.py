from crewai import Agent

class SummaryAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Agente de Resumo",
            goal="Gerar um resumo completo do processamento da nota fiscal",
            backstory=(
                "Especialista em sintetizar e explicar os resultados obtidos por outros agentes "
                "de forma clara e útil ao usuário final, com foco em análise hospitalar e compras médicas."
            )
        )