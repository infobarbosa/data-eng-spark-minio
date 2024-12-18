# Spark / MinIO
Author: Prof. Barbosa<br>
Contact: infobarbosa@gmail.com<br>
Github: [infobarbosa](https://github.com/infobarbosa)

## Objetivo
O objetivo deste laboratório é oferecer ao aluno uma visão prática de como integrar o [Apache Spark](https://spark.apache.org/) com o [MinIO](https://min.io/). Através de exemplos práticos, o aluno aprenderá a configurar e utilizar essas ferramentas para processar e armazenar grandes volumes de dados de forma eficiente.

## Ambiente 
Este laborarório pode ser executado em qualquer estação de trabalho.<br>
Recomendo, porém, a execução em Linux.<br>
Caso você não tenha um à sua disposição, existe a opção do AWS Cloud9: siga essas [instruções](Cloud9/README.md).

# Parte 1 - Setup
Para começar, faça o clone deste repositório:
```sh
git clone https://github.com/infobarbosa/data-eng-spark-minio

```

>### Atenção! 
> Os comandos desse tutorial presumem que você está no diretório raiz do projeto.

```sh
cd data-eng-spark-minio

```

## Docker
Por simplicidade, vamos trabalhar um ambiente baseado em **Docker**.<br>
Na raiz do projeto está disponível um arquivo `compose.yaml` que contém os parâmetros de inicialização do container Docker.<br>
Embora não seja escopo deste laboratório o entendimento detalhado do Docker, recomendo o estudo do arquivo `compose.yaml`.

```sh
ls -la compose.yaml

```

Output esperado:
```
-rw-r--r--  1 barbosa  staff  2392 17 Dez 10:18 compose.yaml
```

## Inicialização
```sh
docker compose up -d

```

Para verificar se está tudo correto:
```sh
docker compose logs -f

```
# Parte 2 - Datasets
### O dataset de clientes
```sh
mkdir -p ./datasets/

```

```sh
curl -L -o ./datasets/clientes.csv.gz https://github.com/infobarbosa/datasets-csv-clientes/raw/refs/heads/main/clientes.csv.gz

```

### O dataset de pedidos
```sh
curl -L -o ./datasets/pedidos-2024-01-01.csv.gz https://github.com/infobarbosa/datasets-csv-pedidos/raw/refs/heads/main/pedidos-2024-01-01.csv.gz

```

# Parte 3 - MinIO

### 1. O bucket `bronze`
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 mb s3://bronze --endpoint-url http://localhost:9000

```

### 2. O bucket `silver`
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 mb s3://silver --endpoint-url http://localhost:9000

```

### 3. O bucket `gold`
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 mb s3://gold --endpoint-url http://localhost:9000

```

### 4. O bucket `scripts`
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 mb s3://scripts --endpoint-url http://localhost:9000

```

### 5. Verificando
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 ls --endpoint-url http://localhost:9000

```

### 6. Upload do arquivo de clientes
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 cp ./datasets/clientes.csv.gz s3://bronze/clientes/clientes.csv.gz \
--endpoint-url http://localhost:9000

```

### 7. Upload do arquivo de pedidos
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 cp ./datasets/pedidos-2024-01-01.csv.gz s3://bronze/pedidos/pedidos-2024-01-01.csv.gz \
--endpoint-url http://localhost:9000

```

### 8. Verificando
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 ls bronze/clientes/ --endpoint-url http://localhost:9000

```

```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 ls bronze/pedidos/ --endpoint-url http://localhost:9000

```

### 9. Upload do script `clientes.py`
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 cp ./scripts/ s3://scripts/ --recursive --endpoint-url http://localhost:9000

```

```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 cp ./scripts/clientes.py s3://scripts/clientes.py \
--endpoint-url http://localhost:9000

```

### 10. Upload do script `pedidos.py`
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 cp ./scripts/pedidos.py s3://scripts/pedidos.py \
--endpoint-url http://localhost:9000

```

### Verificando a pasta `scripts`
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 ls scripts/ --endpoint-url http://localhost:9000

```

# Parte 4 - Tabelas

### Criando o database `ecommerce`
```sh
docker exec -it spark-master spark-sql -e "CREATE DATABASE IF NOT EXISTS ecommerce"

```

### Verificando
```sh
docker exec -it spark-master spark-sql -e "DESCRIBE DATABASE ecommerce"

```

### Criando a tabela `clientes`
```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
CREATE TABLE IF NOT EXISTS ecommerce.clientes (
    ID LONG,
    NOME STRING,
    DATA_NASC DATE,
    CPF STRING,
    EMAIL STRING
)
USING csv
OPTIONS (
    path 's3a://bronze/clientes/',
    header 'true',
    delimiter ';',
    compression 'gzip'
)"

```

### Verificando
```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
SELECT * FROM ecommerce.clientes LIMIT 2"

```

```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
DESCRIBE TABLE ecommerce.clientes"

```
### Criando a tabela `pedidos`
```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
CREATE TABLE IF NOT EXISTS ecommerce.pedidos (
    ID_PEDIDO STRING,
    PRODUTO STRING,
    VALOR_UNITARIO FLOAT,
    QUANTIDADE LONG,
    DATA_CRIACAO DATE,
    UF STRING,
    ID_CLIENTE LONG
)
USING csv
OPTIONS (
    path 's3a://bronze/pedidos/',
    header 'true',
    delimiter ';',
    compression 'gzip'
)"

```

### Verificando
```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
SELECT * FROM ecommerce.pedidos LIMIT 2"

```

```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
DESCRIBE TABLE ecommerce.pedidos"

```

### Criando a tabela `clientes_silver`
```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
CREATE TABLE ecommerce.clientes_silver (
    ID LONG,
    NOME STRING,
    DATA_NASC DATE,
    CPF STRING,
    EMAIL STRING
)
USING parquet
OPTIONS (
    path 's3a://silver/clientes/',
    compression 'snappy'
)"

```

### Verificando
```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
DESCRIBE TABLE ecommerce.clientes_silver"

```

```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
SELECT * FROM ecommerce.clientes_silver LIMIT 2"

```

### Criando a tabela `pedidos_silver`
```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
CREATE TABLE ecommerce.pedidos_silver (
    ID_PEDIDO STRING,
    PRODUTO STRING,
    VALOR_UNITARIO FLOAT,
    QUANTIDADE LONG,
    DATA_CRIACAO DATE,
    UF STRING,
    ID_CLIENTE LONG
)
USING parquet
OPTIONS (
    path 's3a://silver/pedidos/',
    compression 'snappy'
)"

```

### Verificando

```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
DESCRIBE TABLE ecommerce.pedidos_silver"

```

```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
SELECT * FROM ecommerce.pedidos_silver LIMIT 2"

```

# Parte 6 - Processamento

### Processando o script `clientes.py`
```sh
docker exec -it \
spark-master spark-submit \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
s3a://scripts/clientes.py

```

```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
SELECT * FROM ecommerce.clientes_silver LIMIT 2"

```

```sh
docker exec -it \
spark-master spark-submit \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
s3a://scripts/clientes-spark-sql.py

```

### Processando o script `pedidos.py`
```sh
docker exec -it \
spark-master spark-submit \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
s3a://scripts/pedidos.py

```

```sh
docker exec -it \
spark-master spark-sql \
--conf spark.hadoop.fs.s3a.access.key=minioadmin \
--conf spark.hadoop.fs.s3a.secret.key=minioadmin \
--conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
--conf spark.hadoop.fs.s3a.path.style.access=true \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem -e "
SELECT * FROM ecommerce.pedidos_silver LIMIT 2"

```
