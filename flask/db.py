import flask
import psycopg2
import psycopg2.extras

dbconn = None

def get_connection():
    global dbconn
    if dbconn is None:
        dbconn = psycopg2.connect(user='quack',database='quack')
    return dbconn

def get_cursor():
    return get_connection().cursor(cursor_factory = psycopg2.extras.DictCursor)

def execute(sql,**params):
    with get_cursor() as cur:
        cur.execute(sql,params)
        print( "inserting id: [{}]".format( cur.fetchone()[0] ) )

def query_one(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql,params)
        return dict(cur.fetchone())

def query_all(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql,params)
        result = cur.fetchall()
        return {i:  dict(result[i]) for i in range(len(result))}

def commit():
    conn = get_connection()
    conn.commit()
    close()

def rollback():
    if hasattr(flask.g,'dbconn'):
        conn = flask.g.dbconn
        conn.rollback()
        close()

def close():
    global dbconn
    conn = dbconn
    conn.close()

execute( "INSERT INTO users ( nick, name, avatar ) VALUES ( 'a.kukhtichev6', 'anton', 'example' ) RETURNING user_id;" )
commit()
