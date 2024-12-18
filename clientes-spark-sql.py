from pyspark.sql import SparkSession

# Inicializa a sessão Spark
spark = SparkSession.builder \
    .appName("Clientes Spark SQL") \
    .getOrCreate()

# Consulta SQL para obter os dados da tabela ecommerce.clientes
query = "SELECT * FROM ecommerce.clientes"

# Executa a consulta SQL
result = spark.sql(query)

# Mostra os resultados
result.show()

# Encerra a sessão Spark
spark.stop()
