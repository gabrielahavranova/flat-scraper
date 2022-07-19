import psycopg2
from flask import Flask
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from http.server import HTTPServer, SimpleHTTPRequestHandler


def getData():
    conn = psycopg2.connect(database="postgres", user='gabi', password='example', host='db', port='5432')
    if conn:
        print("SUCCESSFULLY CONNECTED TO THE DB!")
    else:
        print("COULD NOT CONNECT TO THE DB!")
    conn.close()


app = Flask(__name__)
@app.route('/')
def renderPage():
    conn = psycopg2.connect(database="postgres", user='gabi', password='example', host='db', port='5432')
    cursor = conn.cursor()
    cursor.execute("select * from flats;")
    res = cursor.fetchall()

    html_source = "<h1>Flats for sale from sreality.cz</h1><br><p>"

    for row in res:
        html_source += f'{row[0]} {row[1]}, {row[2]}<br> <img src="{row[3]}" <br><br><br>'
    html_source+= "</p>"

    return html_source if cursor else "SOMETHING WENT WRONG :("


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')