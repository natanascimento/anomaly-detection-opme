from crewai import Agent

class AnomalyDetectorAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Anomaly Detection Agent',
            goal='Detectar produtos anômalos ou suspeitos na nota fiscal',
            backstory='Especialista em encontrar inconsistências e valores fora do padrão.',
            verbose=True,
        )

    def run(self, items):
        anomalias = []
        for item in items:
            if 'kit' in item.lower() or '9999' in item:
                anomalias.append(item)
        return {'anomalies': anomalias}
