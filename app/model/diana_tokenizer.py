import scispacy
import spacy
import sqlite3
import os.path
from pathlib import Path

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

    # print(token_list)
    BASE_URL = Path(os.path.dirname(os.path.abspath(__file__))).parent
    DB_URL = os.path.join(BASE_URL, DB_NAME)

    conn = sqlite3.connect(DB_URL)
    c = conn.cursor()

    result_data = []
    for token in token_list:
        # print(token)
        c.execute("SELECT * FROM t WHERE key=? COLLATE NOCASE", (token,))
        c.commit()
        origin = c.fetchall()
        if not origin:
            c.execute("SELECT * FROM t WHERE key like ? COLLATE NOCASE", (token,))
            c.commit()
            result = c.fetchall()
            if result:
                result_data.append({token : result})
        else:
            result_data.append({token : origin})
        
    c.close()
    return result_data

def sci_tokenizer(ocr_text):
    
    doc = nlp(ocr_text)
    tokenizer = list(map(str, list(doc.ents)))
    

    return tokenizer
    

