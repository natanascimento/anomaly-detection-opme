from crewai import Agent

class ClassifierAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Classifier Agent',
            goal='Classificar os produtos em OPME, Medicamentos ou Consumo',
            backstory='Treinado com categorias de produtos hospitalares e normas da ANVISA.',
            verbose=True,
        )

    def run(self, items):
        result = []
        for item in items:
            if 'parafuso' in item.lower() or 'placa' in item.lower():
                categoria = 'OPME'
            elif 'dipirona' in item.lower():
                categoria = 'Medicamento'
            else:
                categoria = 'Material de Consumo'
            result.append({'item': item, 'categoria': categoria})
        return {'classified': result}
