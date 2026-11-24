import os
import dotenv

import sqlalchemy

dotenv.load_dotenv()

db_engine = None

def get_engine():
    global db_engine

    if db_engine is None:
        user    = os.environ["DB_USER"]
        senha   = os.environ["DB_PASSWORD"]
        host    = os.environ.get("DB_HOST", "localhost")
        porta   = os.environ.get("DB_PORT", "3306")
        nome_db = os.environ["DB_NAME"]

        url = f"mysql+pymysql://{user}:{senha}@{host}:{porta}/{nome_db}"
        db_engine = sqlalchemy.create_engine(url, pool_recycle=3600)

    return db_engine
