import pandas as pd
from sqlalchemy import create_engine
import uuid

def get_most_recent_session():
    engine = create_engine('postgresql://dgraymullen:bLackie9a@localhost:5432/calibrexml')
    with engine.connect() as connection:
        df = pd.read_sql_query(
            'SELECT raws.* FROM raws INNER JOIN (SELECT sid FROM sessions ORDER BY create_time DESC LIMIT 1) as a ON raws.sid=a.sid',
            connection
        )
        df.drop('sid', inplace=True, axis=1)
        return df


def get_data():
    return [
        {"x": 10, "y": 0 },
        {"x": 40, "y": 90},
        {"x": 80, "y": 50}
    ]
