import psycopg2
import os
import logging
from pathlib import Path
from pathlib import PurePath

from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

def main():
    load_dotenv()
    conn_params = {
        'drivername': 'postgresql+psycopg2',
        'database': os.environ.get('PG_DB_NAME'),
        'username': os.environ.get('PG_USER'),
        'password': os.environ.get('PG_PASSWORD'),
        'host': os.environ.get('PG_HOST'),
        'port': os.environ.get('PG_PORT'),
    }
    schema = os.environ.get('PG_SCHEMA')
    url = URL.create(**conn_params)
    conn = psycopg2.connect(url)
    curs = conn.cursor()

    data_dir = os.environ.get('DATA_DIR')
    if not data_dir.exists():
        os.mkdir(data_dir)

    sql_dir = os.environ.get('SQL_DIR')
    sql_path = Path(
        PurePath(Path(sql_dir)),
    )
    if not sql_path.exists():
        raise FileExistsError(f"SQL DIR NOT EXISTS")

    for sql_file in sql_path.glob('*/*.sql'):
        sql = open(sql_file, encoding='utf-8').read()
        curs.execute(sql)


if __name__ == "__main__":


