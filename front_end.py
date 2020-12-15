import sys
sys.path.append('C:\\Users\\Irene Pan\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages')
from flask import Flask,render_template,request
from rank_bm25 import BM25Okapi
import csv
import pandas as pd
import sqlite3


app = Flask(__name__)
connection = sqlite3.connect("news.db")
cursor = connection.cursor()
query = "SELECT name,url FROM job GROUP BY name"
result = cursor.execute(query).fetchall()
connection.close()


@app.route("/", methods=['GET', 'POST'])
def index():
    resultArray = []
    input = request.form.get("search")
    if input == None:
        return render_template("search.html", input=input, resultArray=resultArray)
    corpus = []
    for str in result:
        if str[0]!=None:
            corpus.append(str[0])
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    query = input
    tokenized_query = query.split(" ")
    doc_scores = bm25.get_scores(tokenized_query) 
    ans=bm25.get_top_n(tokenized_query, corpus, n=10)
    urls_link=[]
    for answers in ans:
        for each in result:
        #print(answers)
            if each[0]==answers:
                print(each[1])
                urls_link.append(each[1])

    for urls_each in urls_link:
        connection = sqlite3.connect("news.db")
        cursor = connection.cursor()
        #print(urls_each)
        ans_query = "SELECT name,url,description FROM job WHERE url='"+urls_each+"' GROUP BY url"
        ans_result = cursor.execute(ans_query).fetchall()
        connection.close()
        resultArray.append(ans_result)
    #process input
    #return resultArray
    return render_template("search.html", input=input, resultArray=resultArray)

if __name__=='__main__':
    app.run(debug=True)
