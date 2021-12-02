from typing import Optional, Text
from fastapi import FastAPI, Request, Form

from pydantic import BaseModel
import json,os
import csv, sqlite3
import nltk


#토크나이저 모델 호출
from model.diana_tokenizer import sci_tokenizer, query_with_token

app = FastAPI()

DB_NAME = "help-diana-word.db"

class DianaText(BaseModel):
    data : list


@app.on_event("startup")
async def dbsetup():
    
    print("HELP DIANA SERVER START")
    nltk.download('punkt')
    if not os.path.isfile(DB_NAME):
        print("---------DB SETUP---------")
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("CREATE TABLE t (key, value, content);")

        with open("merge_dic.csv", 'r', encoding="utf-8") as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['key'], i['value'], i['content']) for i in dr]


        cur.executemany("INSERT INTO t (key, value, content) VALUES (? , ? , ?);", to_db)
        con.commit()
        con.close()
        print("---------DB SETUP END---------")
    else:
        print("---------ALREADY DB EXISTS---------")

@app.get("/algo-api/")
def read_root():
    return {"message": "auto-ta-ml-server"}


@app.post("/algo-api/tokenizer")
def tokenizer(text:DianaText):
    diagnose_data = text.data[0]
    #for test  --> check sample.json
    
    #Tokenizeing
    edited_text = sci_tokenizer(diagnose_data)
    print(edited_text)

    #DB Search
    data = query_with_token(edited_text)

    print(data)
    res = {}
    res['data'] = data

    return res


#db 관련 


if __name__ == "__main__":
    #csv db를 sqlte로 미
    print("server start")
    uvicorn.run(app, host="127.0.0.1", port=8000)
    #for producton
    #uvicorn main:app --host=0.0.0.0 --port=8000 &

    #for test
    #uvicorn main:app --host=0.0.0.0 --port=8000 --reload