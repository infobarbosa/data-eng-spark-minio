from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, LongType, StringType, DateType

# Inicializa a sessão Spark
spark = SparkSession.builder \
    .appName("Clientes CSV to Parquet") \
    .getOrCreate()

# Configurações para acessar o MinIO
spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minioadmin")
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "minioadmin")
spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
spark._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

# Define o esquema para o CSV
schema = StructType([
    StructField("ID", LongType(), True),
    StructField("NOME", StringType(), True),
    StructField("DATA_NASC", DateType(), True),
    StructField("CPF", StringType(), True),
    StructField("EMAIL", StringType(), True)
])

# Lê a tabela clientes em formato CSV com o esquema definido
clientes_df = spark.read \
    .format("csv") \
    .schema(schema) \
    .option("header", "true") \
    .option("delimiter", ";") \
    .option("compression", "gzip") \
    .load("s3a://bronze/clientes/")

# Escreve o DataFrame em formato Parquet no bucket silver
clientes_df.write \
    .mode("overwrite") \
    .parquet("s3a://silver/clientes/")

# Encerra a sessão Spark
spark.stop()
