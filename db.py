import sqlite3

DB_FILE = '/etc/x-ui/x-ui.db'


def get_connection(db_file):
    conn = sqlite3.connect(f'file:{db_file}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def get_inbounds_row(uuid):
    try:
        conn = get_connection(DB_FILE)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM inbounds WHERE json_extract(settings, '$.clients[0].id') = (?)",
            (uuid,),
        )
        return cur.fetchone()
    finally:
        conn.close()
