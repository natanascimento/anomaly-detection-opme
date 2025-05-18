from crewai import Agent

class NormalizerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Normalizer Agent',
            goal='Padronizar nomes de produtos com base em nomenclaturas esperadas',
            backstory='Conhece as principais variações nos nomes de produtos médicos.',
            verbose=True,
        )

    def run(self, items):
        normalized = []
        for item in items:
            norm_item = item.replace("Titânio", "Titânio").replace("4mm", "Ø4mm")
            normalized.append(norm_item)
        return {'normalized': normalized}
