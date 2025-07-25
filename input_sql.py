"""
Script para processar dados de vendas online e gerar arquivos SQL
Converte dados de um CSV em tabelas normalizadas e gera scripts de inserção SQL
"""

import pandas as pd
import os
from pathlib import Path


class SalesDataProcessor:
    """Classe principal para processar dados de vendas e gerar SQL"""

    def __init__(self, csv_path: str, output_dir: str = "input_sql"):
        self.csv_path = csv_path
        self.output_dir = Path(output_dir)
        self.df = None

        # Mapeamento de colunas para padronização
        self.column_mapping = {
            "Transaction ID": "transaction_id",
            "Date": "date",
            "Product Category": "category_name",
            "Product Name": "product_name",
            "Units Sold": "units_sold",
            "Unit Price": "units_price",
            "Total Revenue": "total_revenue",
            "Region": "region",
            "Payment Method": "payment_method",
        }

    # ---------------------- LOAD DATA ----------------------
    def load_and_prepare_data(self) -> pd.DataFrame:
        """Carrega e prepara os dados do CSV"""

        print(f"Carregando dados do CSV: {self.csv_path}")

        self.df = pd.read_csv(self.csv_path)
        print(f"Dados carregados: {len(self.df)} registros\n")

        # Renomear colunas
        self.df.rename(columns=self.column_mapping, inplace=True)

        # Converter data
        self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m-%d")

        print(self.df.head())
        print("\n✅ Dados preparados com sucesso")
        print("-" * 75)
        return self.df

    # ---------------------- EXTRACT ENTITIES ----------------------
    def extract_categories(self) -> pd.DataFrame:
        """Extrai categorias únicas e atribui IDs"""

        print("\nExtraindo categorias...\n")

        categories = pd.DataFrame(
            self.df["category_name"].unique(), columns=["category_name"]
        )
        categories["category_id"] = range(1, len(categories) + 1)
        print(categories.head())
        print("\n✅ Categorias extraidas com sucesso")
        print("-" * 75)
        return categories

    def extract_products(self, categories: pd.DataFrame) -> pd.DataFrame:
        """Extrai produtos únicos e associa ao category_id"""

        print("\nExtraindo produtos...\n")

        # Pega produtos únicos por nome e categoria
        products = self.df[["product_name", "category_name"]].drop_duplicates()
        products = products.merge(categories, on="category_name", how="left")
        products["product_id"] = range(1, len(products) + 1)

        print(products.head())
        print("\n✅ Produtos extraidos com sucesso")
        print("-" * 75)
        return products

    def extract_regions(self) -> pd.DataFrame:
        """Extrai regiões únicas e atribui IDs"""

        print("\nExtraindo regiões...\n")

        regions = pd.DataFrame(self.df["region"].unique(), columns=["region"])
        regions["region_id"] = range(1, len(regions) + 1)

        print(regions.head())
        print("\n✅ Regiões extraidas com sucesso")
        print("-" * 75)
        return regions

    def extract_payment_methods(self) -> pd.DataFrame:
        """Extrai métodos de pagamento únicos e atribui IDs"""

        print("\nExtraindo métodos de pagamento...\n")

        payment_methods = pd.DataFrame(
            self.df["payment_method"].unique(), columns=["payment_method"]
        )
        payment_methods["payment_id"] = range(1, len(payment_methods) + 1)

        print(payment_methods.head())
        print("\n✅ Métodos de pagamento extraidos com sucesso")
        print("-" * 75)
        return payment_methods

    # ---------------------- CREATE ORDERS TABLE ----------------------
    def create_orders_table(
        self,
        products: pd.DataFrame,
        regions: pd.DataFrame,
        payment_methods: pd.DataFrame,
        categories: pd.DataFrame,
    ) -> pd.DataFrame:
        """Cria a tabela de pedidos com IDs relacionados"""

        print("\nCriando tabela de pedidos...\n")

        orders = self.df[
            [
                "transaction_id",
                "date",
                "product_name",
                "units_sold",
                "units_price",
                "total_revenue",
                "region",
                "payment_method",
            ]
        ].copy()

        # Merge para obter os IDs
        orders = orders.merge(
            products[["product_name", "product_id"]], on="product_name", how="left"
        )
        orders = orders.merge(regions, on="region", how="left")
        orders = orders.merge(payment_methods, on="payment_method", how="left")

        # Selecionar apenas as colunas necessárias
        orders = orders[
            [
                "transaction_id",
                "date",
                "product_id",
                "units_sold",
                "units_price",
                "total_revenue",
                "region_id",
                "payment_id",
            ]
        ]

        # Remover duplicatas com base no transaction_id
        orders = orders.drop_duplicates(subset=["transaction_id"])

        print(orders.head())
        print("\n✅ Tabela de pedidos criada com sucesso")
        print("-" * 75)
        return orders

    # ---------------------- OUTPUT SQL FILES ----------------------
    def create_output_directory(self):
        """Cria o diretório de saída se não existir"""

        self.output_dir.mkdir(exist_ok=True)
        print(f"\nGerando arquivos SQL no diretório de saída: {self.output_dir}\n")

    # ---------------------- GENERATE SQL FILES ----------------------
    def escape_sql_string(self, text: str) -> str:
        """Escapa aspas simples em strings SQL"""

        return str(text).replace("'", "''")

    ##################### CATEGORY #####################
    def generate_categories_sql(self, categories: pd.DataFrame):
        """Gera arquivo SQL para categorias"""

        file_path = self.output_dir / "categories.sql"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("-- Inserção de Categorias\n")
            for category in categories["category_name"]:
                escaped_category = self.escape_sql_string(category)
                file.write(
                    f"INSERT INTO categories (category_name) VALUES ('{escaped_category}');\n"
                )

        print(f"✅ Arquivo de CATEGORIAS criado com sucesso")

    ##################### PRODUCTS #####################
    def generate_products_sql(self, products: pd.DataFrame):
        """Gera arquivo SQL para produtos"""

        file_path = self.output_dir / "products.sql"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("-- Inserção de Produtos\n")
            for _, row in products.iterrows():
                name = self.escape_sql_string(row["product_name"])
                category_id = row["category_id"]
                product_id = row["product_id"]
                file.write(
                    f"INSERT INTO products (id, product_name, category_id) VALUES ({product_id}, '{name}', {category_id});\n"
                )

        print(f"✅ Arquivo de PRODUTOS criado com sucesso")

    ##################### REGIONS #####################
    def generate_regions_sql(self, regions: pd.DataFrame):
        """Gera arquivo SQL para regiões"""

        file_path = self.output_dir / "regions.sql"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("-- Inserção de Regiões\n")
            for region in regions["region"]:
                escaped_region = self.escape_sql_string(region)
                file.write(f"INSERT INTO regions (name) VALUES ('{escaped_region}');\n")

        print(f"✅ Arquivo de REGIÕES criado com sucesso")

    ##################### PAYMENT METHODS #####################
    def generate_payment_methods_sql(self, payment_methods: pd.DataFrame):
        """Gera arquivo SQL para métodos de pagamento"""

        file_path = self.output_dir / "payment_methods.sql"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("-- Inserção de Métodos de Pagamento\n")
            for method in payment_methods["payment_method"]:
                escaped_method = self.escape_sql_string(method)
                file.write(
                    f"INSERT INTO payment_methods (method) VALUES ('{escaped_method}');\n"
                )

        print(f"✅ Arquivo de MÉTODOS DE PAGAMENTO criado com sucesso")

    ##################### ORDERS #####################
    def generate_orders_sql(self, orders: pd.DataFrame):
        """Gera arquivo SQL para pedidos"""

        file_path = self.output_dir / "orders.sql"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("-- Inserção de Pedidos\n")
            for _, row in orders.iterrows():
                file.write(
                    f"INSERT INTO orders (transaction_id, order_date, product_id, quantity, unit_price, total_price, region_id, payment_method_id) VALUES "
                    f"('{row['transaction_id']}', '{row['date'].date()}', {row['product_id']}, {row['units_sold']}, {row['units_price']:.2f}, {row['total_revenue']:.2f}, {row['region_id']}, {row['payment_id']});\n"
                )

        print(f"✅ Arquivo de ORDENS criado com sucesso")

    def process_all(self):
        """Executa todo o processo de conversão"""

        print("🚀 Iniciando processamento dos dados de vendas...\n")

        # 1. Carregar e preparar dados
        self.load_and_prepare_data()

        # 2. Extrair entidades
        categories = self.extract_categories()
        products = self.extract_products(categories)
        regions = self.extract_regions()
        payment_methods = self.extract_payment_methods()

        # 3. Criar tabela de pedidos
        orders = self.create_orders_table(
            products, regions, payment_methods, categories
        )

        # 4. Criar diretório de saída
        self.create_output_directory()

        # 5. Gerar arquivos SQL
        self.generate_categories_sql(categories)
        self.generate_products_sql(products)
        self.generate_regions_sql(regions)
        self.generate_payment_methods_sql(payment_methods)
        self.generate_orders_sql(orders)

        print("-" * 75)

        # Estatísticas finais
        print("\n📊 Estatísticas:")
        print(f"   • Categorias: {len(categories)}")
        print(f"   • Produtos: {len(products)}")
        print(f"   • Regiões: {len(regions)}")
        print(f"   • Métodos de pagamento: {len(payment_methods)}")
        print(f"   • Pedidos: {len(orders)}")


def main():
    """Função principal para executar o processamento"""

    # Configurações
    csv_file = "data/raw/Online Sales Data.csv"

    # Verificar se o arquivo existe
    if not os.path.exists(csv_file):
        print(f"❌ Erro: Arquivo não encontrado: {csv_file}")
        return

    # Executar processamento
    processor = SalesDataProcessor(csv_file)
    processor.process_all()


if __name__ == "__main__":
    main()
