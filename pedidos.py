from pyspark.sql import SparkSession

# Inicializa a sessão Spark
spark = SparkSession.builder \
    .appName("Pedidos CSV to Parquet") \
    .getOrCreate()

# Configurações para acessar o MinIO
spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minioadmin")
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "minioadmin")
spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
spark._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

# Lê a tabela pedidos em formato CSV
pedidos_df = spark.read \
    .format("csv") \
    .option("header", "true") \
    .option("delimiter", ";") \
    .option("compression", "gzip") \
    .load("s3a://bronze/pedidos/")

# Escreve o DataFrame em formato Parquet no bucket silver
pedidos_df.write \
    .mode("overwrite") \
    .parquet("s3a://silver/pedidos/")

# Encerra a sessão Spark
spark.stop()
