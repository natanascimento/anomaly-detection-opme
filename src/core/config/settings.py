from os.path import abspath, dirname, join
from os import environ
import dotenv

class AppSettings:
    APP_NAME = "Anomaly Detection Agent"
    ROOT_PATH = dirname(dirname(dirname(dirname(abspath(__file__)))))
    PROJECT_PATH = dirname(dirname(dirname(abspath(__file__))))
    LOGS_PATH = join(ROOT_PATH, "logs")
    DATA_PATH = join(ROOT_PATH, "data")
    ENV = environ.get('ENV')

class OpenAiSettings:
    AUTH_TOKEN = environ.get('OPENAI_API_KEY')

class Settings:
    dotenv.load_dotenv(dotenv.find_dotenv())
    app: AppSettings = AppSettings()
    oai: OpenAiSettings = OpenAiSettings()
