import os
from pathlib import Path, PurePath

from dotenv import load_dotenv

from models import ExtractSettings, LoadSettings, TransformSettings


class Config:

    def __init__(self):
        load_dotenv()

        # Settings for PostgresExtractor.
        pg_conn_params = {
            'dbname': os.environ['PG_DB_NAME'],
            'user': os.environ['PG_USER'],
            'password': os.environ['PG_PASSWORD'],
            'host': os.environ['PG_HOST'],
            'port': os.environ['PG_PORT'],
        }
        pg_schema = os.environ['PG_SCHEMA']
        batches = os.environ['BATCHES']
        pg_extract_dir = os.environ['EXTRACT_DATA_DIR']
        pg_extract_path = Path(pg_extract_dir)
        sql_dir = os.environ['SQL_DIR']
        sql_extract_file_name = os.environ['SQL_EXTRACT_FILE_NAME']
        if not pg_extract_path.exists():
            os.mkdir(pg_extract_dir)
        sql_path = Path(
            PurePath(Path(sql_dir)),
        )
        if not sql_path.exists():
            raise FileExistsError(f"SQL DIR NOT EXISTS")
        sql_extract_file_path = Path(
            PurePath(
                sql_path,
                sql_extract_file_name
            )
        )
        if not sql_extract_file_path.exists():
            raise FileExistsError(f"SQL EXTRACT FILE NOT EXISTS")

        # Settings for DataTransform.
        transform_dir = os.environ['TRANSFORM_DATA_DIR']
        transform_path = Path(transform_dir)
        if not transform_path.exists():
            os.mkdir(transform_dir)

        # Settings for ElasticsearchLoader.
        es_host = os.environ['ES_HOST']
        es_port = os.environ['ES_PORT']
        es_conn_str = f"http://{es_host}:{es_port}"
        es_index = os.environ['ES_INDEX']
        es_settings_dir = os.environ['ES_SETTINGS_PATH']
        es_settings_path = Path(es_settings_dir)
        if not es_settings_path.exists():
            raise FileExistsError(f"ES SETTINGS DIR NOT EXISTS")
        es_schema_file_name = os.environ['ES_SCHEMA_FILE']
        es_schema_file_path = Path(
            PurePath(
                es_settings_path,
                es_schema_file_name
            )
        )
        if not es_schema_file_path.exists():
            raise FileExistsError(f"ES SCHEMA FILE NOT EXISTS")

        self.extract_settings = ExtractSettings(
            conn_params=pg_conn_params,
            schemas=pg_schema,
            extract_path=pg_extract_path,
            sql_file=sql_extract_file_path,
            batches=batches,
        )
        self.transform_settings = TransformSettings(
            transform_path=transform_path,
            extract_path=pg_extract_path,
            index_name=es_index,
        )
        self.load_settings = LoadSettings(
            conn_str=es_conn_str,
            index_name=es_index,
            transform_path=transform_path,
            schema_file_path=es_schema_file_path,
        )
