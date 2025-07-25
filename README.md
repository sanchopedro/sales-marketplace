# Sales Marketplace - ETL e Dashboard

Este projeto realiza o processamento de dados de vendas online, desde a extração dos dados brutos via API do Kaggle, normalização e geração de scripts SQL para popular um banco de dados relacional, até a visualização analítica em um dashboard Power BI.

A fonte dos dados brutos, obtidos pelo Kaggle, pode ser acessada [neste link](https://www.kaggle.com/datasets/shreyanshverma27/online-sales-dataset-popular-marketplace-data/data).

---

## 📁 Estrutura do Projeto

```
sales-marketplace/
│
├── data/
│   └── raw/
│       └── Online Sales Data.csv
│
├── input_sql/
│   ├── categories.sql
│   ├── products.sql
│   ├── regions.sql
│   ├── payment_methods.sql
│   └── orders.sql
│
├── dashboard/
│   └── [Arquivo Power BI .pbix]
│
├── create_database.sql
├── input_sql.py
├── get_data.py
├── requirements.txt
└── README.md
```

---

## 🚀 Passo a Passo

### 1. **Preparação do Ambiente**

- Certifique-se de ter o Python 3.8+ instalado.
- Instale as dependências do projeto:

  ```bash
  pip install -r requirements.txt
  ```

### 2. **Extração dos Dados Brutos**

- Execute o script `get_data.py` para baixar os dados do Kaggle via API e salvar em `data/raw/Online Sales Data.csv`.
- Certifique-se de ter configurado sua API Key do Kaggle conforme a [documentação oficial](https://github.com/Kaggle/kaggle-api#api-credentials).

  ```bash
  python get_data.py
  ```

### 3. **Criação do Banco de Dados**

- Execute o script SQL para criar as tabelas no MySQL:

  ```sql
  SOURCE create_database.sql;
  ```

### 4. **Geração dos Scripts de Inserção SQL**

- Execute o script Python principal para processar o CSV e gerar os arquivos SQL de inserção:

  ```bash
  python input_sql.py
  ```

### 5. **Carregamento dos Dados no Banco**

- Importe os dados para as tabelas correspondentes usando os scripts SQL gerados em `input_sql/`:

  ```sql
  SOURCE input_sql/categories.sql;
  SOURCE input_sql/products.sql;
  SOURCE input_sql/regions.sql;
  SOURCE input_sql/payment_methods.sql;
  SOURCE input_sql/orders.sql;
  ```

### 6. **Criação e Atualização do Dashboard**

- Abra o arquivo `.pbix` na pasta `dashboard/` com o Power BI Desktop.
- Atualize a conexão com o banco de dados MySQL, se necessário.
- O dashboard será atualizado automaticamente com os dados mais recentes.

---

## 📊 Dashboard

O dashboard Power BI fornece insights sobre as vendas, incluindo:

- Total de vendas por região
- Produtos mais vendidos
- Métodos de pagamento mais populares
- Análise temporal das vendas

---

## ⚙️ Tecnologias Utilizadas

- Python 3.8+
- Pandas
- MySQL
- Power BI
- [Kaggle API](https://github.com/Kaggle/kaggle-api)



