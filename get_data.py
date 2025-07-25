import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Caminho do arquivo kaggle.json
KAGGLE_JSON_PATH = "./secrets/kaggle.json"

# Diretório onde os dados serão salvos
DOWNLOAD_DIR = "data/raw"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Configura a variável de ambiente para autenticação
os.environ['KAGGLE_CONFIG_DIR'] = os.path.dirname(KAGGLE_JSON_PATH)

# Inicializa a API do Kaggle
api = KaggleApi()
api.authenticate()

# Dataset a ser baixado (slug extraído da URL)
dataset_slug = "shreyanshverma27/online-sales-dataset-popular-marketplace-data"

# Baixa o dataset
api.dataset_download_files(dataset_slug, path=DOWNLOAD_DIR, unzip=True)

print(f"Dataset baixado e salvo em: {DOWNLOAD_DIR}")
