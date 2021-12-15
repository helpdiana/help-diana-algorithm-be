import scispacy
import spacy
import sqlite3
import os.path
from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize
import re
import numpy as np

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
def query_with_token(token_list):
    #print('token_list  ',token_list)
    #print('========================================================')
    BASE_URL = Path(os.path.dirname(os.path.abspath(__file__))).parent
    DB_URL = os.path.join(BASE_URL, DB_NAME)

    conn = sqlite3.connect(DB_URL)
    c = conn.cursor()

    result_data = []
    #token_list에 토크나이저로 뽑아진 의학단어들이 들어 있음 ex) ['LUL','benign-looking noudle','LNE']
    #각 token들을 하나씩 검사
    for token in token_list:
        korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
        #print(type(token))
        #print('ko 전')
        #한국어 제거
        token = re.sub(korean,"",token)
        #1. 의학 단어 사전에서 token과 일치하는 것이 있다면,(이때 대소문자 구분 안함)
        
        c.execute("SELECT * FROM t WHERE key= ? COLLATE NOCASE", (token,))
        conn.commit()
        #2. 그에 대한 (key,value,content) 전부 검색해서 가지고 옴.
        origin = c.fetchall()

        result_data.append({token : origin})

        #print('들어옴')
        #현재 token을 다시 word 
        token_word_list = word_tokenize(token)
        if len(token_word_list) > 1 :
            for token_word in token_word_list:
                print('token_word',token_word)
                print('==============================================================')
                token_word = re.sub(korean,"",token_word)
                c.execute("SELECT * FROM t WHERE key= ? COLLATE NOCASE", (token_word,))
                conn.commit()
                result_t = c.fetchall()
                print('단어 같은거 있냐')
                print(result_t)
                if result_t:
                    result_data.append({token : result_t})
                

                print('==============================================================')

                #token_word = " {0} ".format(token_word)
                token_word1 = " {0}".format(token_word)
                token_word2 =  "{0} ".format(token_word)
                s = "SELECT * FROM t WHERE key LIKE '%{0}%' OR key LIKE '%{1}%' COLLATE NOCASE".format(token_word1,token_word2)
                #s = "SELECT * FROM t WHERE key LIKE '%{0}%' COLLATE NOCASE".format(token_word)

                c.execute(s)
                conn.commit()
                print('result')
                print(token_word,'를 포함하고 있는 단어들')
                result = c.fetchall()
                print(result)
                #print('==========================================================')

                #print("현재 검사중인 단어")
                t = " {0} ".format(token)
                print(t)
                if result :
                    #print('있는지 검사할 애들')
                    k = np.array(result).T[0]
                    print(k)
                    for i in range(0,len(k)):
                        m = " {0} ".format(k[i])
                        print(m)
                        #print('------>',m[1:-1])
                        if m in t :
                            index = k.tolist().index(m[1:-1])
                            #print('------>',m[1:-1])
                            #print(index)
                            if m[1:-1].lower() != token.lower():
                                result_data.append({token : result[index]})
                                
                                #print('*****************************************************************************')

                
        
    conn.close()
    return result_data

def sci_tokenizer(ocr_text):
    
    doc = nlp(ocr_text)
    tokenizer = list(map(str, list(doc.ents)))
    

    return tokenizer
    

