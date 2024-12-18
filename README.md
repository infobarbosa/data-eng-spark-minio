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
mkdir ./datasets/

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

### 4. Verificando
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 ls --endpoint-url http://localhost:9000

```

### 5. Upload do arquivo de clientes
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 cp ./datasets/clientes.csv.gz s3://bronze/clientes/clientes.csv.gz \
--endpoint-url http://localhost:9000

```

### 6. Upload do arquivo de pedidos
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 cp ./datasets/pedidos-2024-01-01.csv.gz s3://bronze/pedidos/pedidos-2024-01-01.csv.gz \
--endpoint-url http://localhost:9000

```

### 7. Verificando
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

# Parte 4 - Spark

### Criando o database `ecommerce`
```sh
docker exec -it spark-master /opt/spark/bin/spark-sql -e "CREATE DATABASE ecommerce"

```

### Criando a tabela `clientes`
```sh
docker exec -it spark-master spark-sql -e "
CREATE TABLE ecommerce.clientes (
    ID LONG,
    NOME STRING,
    DATA_NASC DATE,
    CPF STRING,
    EMAIL STRING
)
USING csv
OPTIONS (
    path 's3a://clientes/clientes.csv.gz',
    header 'true',
    delimiter ';',
    compression 'gzip'
)"
```

### Criando a tabela `pedidos`
```sh
docker exec -it spark-master /opt/spark/bin/spark-sql -e "
CREATE TABLE ecommerce.pedidos (
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
    path 's3a://clientes/pedidos-2024-01-01.csv.gz',
    header 'true',
    delimiter ';',
    compression 'gzip'
)"
```