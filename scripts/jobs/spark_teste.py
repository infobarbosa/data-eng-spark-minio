from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("HiveIntegrationTest") \
        .enableHiveSupport() \
        .getOrCreate()
    
    # Lista os databases existentes
    spark.sql("SHOW DATABASES").show()

    # Cria um database teste
    spark.sql("CREATE DATABASE IF NOT EXISTS database_teste")
    
    # Cria uma tabela (se não existir)
    spark.sql("CREATE TABLE IF NOT EXISTS database_teste.tabela_teste (id INT, name STRING)")
    
    # Insere alguns dados na tabela
    spark.sql("INSERT INTO database_teste.tabela_teste VALUES (1, 'Barbosa'), (2, 'Marcelo')")
    
    # Lê de volta para confirmar
    df = spark.sql("SELECT * FROM database_teste.tabela_teste")
    df.show()
    
    spark.stop()

if __name__ == "__main__":
    main()
