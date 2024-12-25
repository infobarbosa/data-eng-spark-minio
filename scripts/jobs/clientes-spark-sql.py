from pyspark.sql import SparkSession

# Inicializa a sessão Spark com configurações para acessar o MinIO
spark = SparkSession.builder \
    .appName("Clientes Spark SQL") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Verifica se a tabela existe listando todas as tabelas no banco de dados ecommerce
spark.sql("SHOW TABLES IN spark_catalog.ecommerce").show()

# Consulta SQL para obter os dados da tabela ecommerce.clientes
query = "SELECT * FROM spark_catalog.ecommerce.clientes"

# Executa a consulta SQL
result = spark.sql(query)

# Mostra os resultados
result.show()

# Encerra a sessão Spark
spark.stop()