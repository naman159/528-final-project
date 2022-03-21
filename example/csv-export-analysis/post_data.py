import psycopg2
import psycopg2.extras
import uuid
import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import dialects

psycopg2.extras.register_uuid()

def new_conn():
    return psycopg2.connect("dbname=calibrexml user=dgraymullen")

# %% create sessions table identifying csv's with a uuid
# CREATE TABLE sessions(
#   sid uuid PRIMARY KEY,
#   create_time timestamp,
#   name varchar
# );

session_name = "test_2"

conn = new_conn()
cur = conn.cursor()

curr_uuid = uuid.uuid4()
cur.execute("INSERT INTO sessions (sid, create_time, name) VALUES (%s, %s, %s)", (curr_uuid, datetime.datetime.now(), session_name))

conn.commit()
cur.close()
conn.close()

# %% write csv with mapper from sqlalchemy

def write_session(csv, current_uuid):
    engine = create_engine('postgresql://dgraymullen:bLackie9a@localhost:5432/calibrexml')
    df = pd.read_csv(csv)
    df = df.rename(columns={'time':'filteredTime', 'rep':'r', 'set':'s'})
    df['sid'] = str(current_uuid)
    df.to_sql('raws', engine, if_exists='append', index=False, dtype={'sid':dialects.postgresql.UUID})

write_session('data/session_0.csv', curr_uuid)

print('inserted data for:', session_name, 'uuid:', curr_uuid)

# %% alter table constraint
conn = new_conn()
cur = conn.cursor()

cur.execute("ALTER TABLE raws ADD CONSTRAINT sessions_id FOREIGN KEY (sid) REFERENCES sessions (sid) MATCH FULL;")

conn.commit()
cur.close()
conn.close()
