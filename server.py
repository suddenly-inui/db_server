import http.server as s
import json
from os import initgroups

import sqlite3
import pandas as pd


class MyHandler(s.BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect("json.db")
        c = conn.cursor()
        db = pd.read_sql("SELECT * FROM users", conn)
        # レスポンス処理
        id_ = 1

        res = {
            "Id": db[db.id == id_].loc[0, "id"],
            "Name": db[db.id == id_].loc[0, "rgname"],
            "KG": db[db.id == id_].loc[0, "kg"]
        }
        self.send_response(200)
        self.send_header("Content-type", "application/json;charset=utf-8")
        self.end_headers()
        body_json = json.dumps(res)
        self.wfile.write(body_json.encode("utf-8"))

        c.close()
        conn.close()


def makedb():
    con = sqlite3.connect("json.db")
    c = con.cursor()
    c.execute('''DROP TABLE IF EXISTS users''')
    c.execute('''CREATE TABLE users(id real, rgname text, kg text)''')
    c.execute("INSERT INTO users VALUES (1, 'inui', 'd-hacks')")
    con.commit()
    con.close()


makedb()
host = "0.0.0.0"
port = 20000
httpd = s.HTTPServer((host, port), MyHandler)
httpd.serve_forever()
