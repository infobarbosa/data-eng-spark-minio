
### Criando o bucket `clientes`
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 mb s3://clientes --endpoint-url http://localhost:9000

```

Verificando:
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 ls --endpoint-url http://localhost:9000

```

### O dataset de clientes
```sh
mkdir ./datasets/

```

```sh
git clone https://github.com/infobarbosa/datasets-csv-clientes ./datasets/

```


### Upload do arquivo csv
```sh
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 cp ./datasets/datasets-csv-clientes/clientes.csv.gz s3://clientes/clientes.csv.gz \
--endpoint-url http://localhost:9000

```


### Verificando o conteúdo do bucket
```
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
aws s3 ls clientes --endpoint-url http://localhost:9000

```
