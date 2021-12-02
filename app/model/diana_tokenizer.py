import scispacy
import spacy
import sqlite3
import os.path
from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize
import re

nlp = spacy.load("en_core_sci_scibert")
DB_NAME = "help-diana-word.db"
# text = """
# Myeloid derived suppressor cells (MDSC) are immature 
# myeloid cells with immunosuppressive activity. 
# They accumulate in tumor-bearing mice and humans 
# with different types of cancer, including hepatocellular 
# carcinoma (HCC). 
# """
# doc = nlp(text)

# print(list(doc.sents))
# print(doc.ents)
def query_with_token(text):
    print('v3')
    BASE_URL = Path(os.path.dirname(os.path.abspath(__file__))).parent
    DB_URL = os.path.join(BASE_URL, DB_NAME)

    conn = sqlite3.connect(DB_URL)
    c = conn.cursor()

    final_result = []

    for token_list in text:

        result_data = []
        for token in token_list:
            korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
            #print(type(token))
            #print('ko 전')
            next_token = re.sub(korean,"",token)
            #print('sub ko token ',next_token)
            c.execute("SELECT * FROM t WHERE key= ? COLLATE NOCASE", (next_token,))
            conn.commit()
            #token있으면 그에 대한 (key,value,content) 전부 검색해서 가지고 옴.
            origin = c.fetchall()
            #print('origin')
            #print(origin)]
            if origin:
                result_data.append({token : origin})

            #c.execute("SELECT * FROM t WHERE key like '%?' COLLATE NOCASE", (token,))
            #s= "SELECT * FROM t WHERE key like '%{0}%' COLLATE NOCASE".format(token)
            #print('들어옴')
            
            '''
            token_word_list = word_tokenize(token)
            if len(token_word_list) > 1 :
                for token_word in token_word_list:
                    token_word = re.sub(korean,"",token_word)
                    c.execute("SELECT * FROM t WHERE key= ? COLLATE NOCASE", (token_word,))
                    conn.commit()
                    result_t = c.fetchall()
                    #print('result_t')
                    #print(result_t)
                    if result_t:
                        result_data.append({token : result_t})

                    token_word = " {0} ".format(token_word)
                    #print(token_word)
                    s = "SELECT * FROM t WHERE key LIKE '%{0}%' COLLATE NOCASE".format(token_word)
                    c.execute(s)
                    conn.commit()
                    result = c.fetchall()
                    #print('result') 
                    #print(result)
                    if result:
                        print("이건 result")
                        print(result)
                        print("----------")
                        result_data.append({token : result})
                '''
        final_result.append(result_data)
        
    conn.close()
    return final_result

def sci_tokenizer(ocr_text):

    tokenizer_list = []
    for text in ocr_text:
        doc = nlp(text[0])
        tokenizer = list(map(str, list(doc.ents)))
        
        tokenizer_list.append(tokenizer)

    print(len(tokenizer_list))
    return tokenizer_list
    
