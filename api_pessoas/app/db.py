import psycopg 
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL)


#  Teste de conexão

# if __name__ == "__main__":
#     try:
#         with get_conn() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT 1;")
#                 print("Conexão OK:", cur.fetchone())
#     except Exception as e:
#         print("Erro ao conectar no banco:", e)
