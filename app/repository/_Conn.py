import psycopg2
import os

from psycopg2 import sql
from contextlib import contextmanager
from dotenv import load_dotenv

class Conn:
    def create_database(self):
        load_dotenv()
        db_name = os.getenv("DB_NAME")
        try:
            with self.get_connect("postgres") as conn:

                conn.autocommit = True
                cursor = conn.cursor()

                cursor.execute("SELECT 1 FROM pg_database WHERE datname = '{}'".format(db_name))
                exists = cursor.fetchone()
                
                if not exists:
                    cursor.execute(sql.SQL("CREATE DATABASE {}".format(db_name)))

                cursor.close()

        except Exception as e:
            print("Erro ao conectar ao banco de dados")
            print(e)
    
    def create_table(self):
        try:
            with self.get_connect() as conn:

                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(100) NOT NULL
                    );
                """)

                conn.commit()
                cursor.close()

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    @contextmanager
    def get_connect(self, database = None):
        load_dotenv()
        
        db_name = database if database else os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")

        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port 
        )
        try:
            yield conn
        finally: 
            conn.close()

        return conn
