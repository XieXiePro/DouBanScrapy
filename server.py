# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template, flash

import pymysql
import json
from bson import json_util

app = Flask(__name__)

def get_conn():
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="xieping",
                           database="estore",)
    return conn

def toJson(data):
    return json.dumps(
               data,
               default=json_util.default,
               ensure_ascii=False
           )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def get_goods():
    if request.method == 'GET':
        conn = get_conn()
        cursor = conn.cursor()
        sql = "select * from DB"
        cursor.execute(sql)
        results = cursor.fetchall()

        resultList = []

        for result in results:
            resultList.append(result)

        return render_template('search.html', entries=resultList)

if __name__ == '__main__':
    app.run(debug=True)