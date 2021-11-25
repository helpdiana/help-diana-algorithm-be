import scispacy
import spacy

nlp = spacy.load("en_core_sci_scibert")
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
def query_with_token():
    pass

def sci_tokenizer(ocr_text):
    
    doc = nlp(ocr_text)
    tokenizer = list(map(str, list(doc.ents)))
    

    return tokenizer
    

