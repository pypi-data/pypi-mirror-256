import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv(dotenv_path=find_dotenv())


def get_engine(target: str, drivername: str = "postgresql+psycopg2"):
    """_summary_

    Args:
        target (str): _description_
        drivername (str, optional): _description_. Defaults to "postgresql+psycopg2".

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    try:
        host = os.environ.get(f"{target}_DB_HOST")
        port = os.environ.get(f"{target}_DB_PORT")
        database = os.environ.get(f"{target}_DB_NAME")
        username = os.environ.get(f"{target}_DB_USERNAME")
        password = os.environ.get(f"{target}_DB_PASSWORD")

        if None in (host, port, database, username, password):
            raise Exception("해당 target의 환경변수를 제대로 입력해주세요.")

        dsn = URL.create(
            drivername=drivername,
            host=host,
            port=port,
            database=database,
            username=username,
            password=password,
        )
        return create_engine(dsn)
    except Exception as error:
        print(error)
