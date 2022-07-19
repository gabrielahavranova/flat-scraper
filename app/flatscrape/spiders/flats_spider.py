import scrapy
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class MySimpleDB:
    def __init__(self, database, user, password, host, port):
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        if not self.conn:
            print("could not establish connection to the db!")
            return
        self.cursor = self.conn.cursor()
        create_db = "CREATE database mydb;"

        # Creating a database
        try:
            self.cursor.execute(create_db)
        except psycopg2.errors.DuplicateDatabase:
            pass

        self.createFlatsTable()
        print("Database created successfully...")

    def createFlatsTable(self):
        try:
            create_table = "CREATE TABLE flats (flat_id SERIAL PRIMARY KEY, flat_name VARCHAR(255) NOT NULL,\
             flat_locality VARCHAR(255) NOT NULL, flat_image_link VARCHAR(255) NOT NULL);"
            self.cursor.execute(create_table)
        except psycopg2.errors.DuplicateTable:
            # table already exists, clear it 
            drop_table = "DELETE FROM flats;"


    def saveFlat(self, name, locality, image_url):
        cmd = "INSERT INTO flats (flat_name,flat_locality,flat_image_link) VALUES \
            ('" + str(name) + "', '" + str(locality) + "', '" + str(image_url) + "');"
        try:
            self.cursor.execute(cmd)
        except:
            pass

    def cleanup(self):
        self.conn.close()


class FlatsSpider(scrapy.Spider):
    name = "flats"
    start_urls = ["https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500"]

    def parse(self, response):
        db = MySimpleDB(database="postgres", user='gabi', password='example', host='db', port='5432')

        src_data = json.loads(response.text)
        i = 1

        for flat in src_data['_embedded']['estates']:
            print((i, flat['name'], flat['locality'], flat['_links']['images'][0]['href']))
            db.saveFlat(flat['name'], flat['locality'], flat['_links']['images'][0]['href'])
            i += 1

        db.cleanup()