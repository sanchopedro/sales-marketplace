-- Criando database
create database online_sales;
use online_sales;

-- #Criando tabelas:
-- 1. Tabela de Categorias
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL
);

-- 2. Tabela de Produtos 
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    UNIQUE (product_name, category_id)
);

-- 3. Tabela de Regiões
CREATE TABLE regions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- 4. Tabela de Métodos de Pagamento
CREATE TABLE payment_methods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    method VARCHAR(100) UNIQUE NOT NULL
);


-- 5. Tabela de Pedidos
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50),
    order_date DATE NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(12, 2) NOT NULL,
    region_id INT,
    payment_method_id INT,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (region_id) REFERENCES regions(id),
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id)
);