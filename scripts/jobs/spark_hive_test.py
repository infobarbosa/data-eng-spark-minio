from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("HiveIntegrationTest") \
        .enableHiveSupport() \
        .getOrCreate()
    
    # Lista os databases existentes
    spark.sql("SHOW DATABASES").show()
    
    # Cria uma tabela (se não existir)
    spark.sql("CREATE TABLE IF NOT EXISTS default.test_table (id INT, name STRING)")
    
    # Insere alguns dados na tabela
    spark.sql("INSERT INTO default.test_table VALUES (1, 'Alice'), (2, 'Bob')")
    
    # Lê de volta para confirmar
    df = spark.sql("SELECT * FROM default.test_table")
    df.show()
    
    spark.stop()

if __name__ == "__main__":
    main()
