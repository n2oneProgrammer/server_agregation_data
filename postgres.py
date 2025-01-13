import os
import psycopg2


def push_command(command: str, params: tuple):
    conn = psycopg2.connect(database="postgres",
                            host=os.environ['POSTGRES_IP'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'],
                            port=int(os.environ['POSTGRES_PORT']))
    cursor = conn.cursor()
    cursor.execute(command, params)
    conn.commit()
    conn.close()
