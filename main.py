import fitz
import streamlit as st
import io
import string
import re
import nltk
from nltk import sent_tokenize,word_tokenize
from nltk.corpus import stopwords  #stopwords
# from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
# stemmer=PorterStemmer()

import pydaisi as pyd
wc = pyd.Daisi("feedexpedition/WordCloud")

def return_doc_from_bytes(pdfbytes):
    doc = fitz.open(stream=pdfbytes)
    return doc

def preprocessing(sentences):
    documents_clean = ''
    for d in sentences:
        # Remove Unicode
        document_test = re.sub('[^a-zA-Z0-9]', ' ', d)
        # Lowercase the document
        document_test = document_test.lower()
        # Remove punctuations
        document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
        #Remove the numbers
        document_test = re.sub(r'[0-9]', '', document_test)
        # Remove the doubled space
        document_test = re.sub(r'\s{2,}', ' ', document_test)
        #tokenization
        document_test = document_test.split()
        #stopwords_removal
        document_test = [word for word in document_test if not word in set(stopwords.words('english'))]
        #stemming
        #document_test = [stemmer.stem(word) for word in document_test]
        #lemmmitization
        document_test = [lemmatizer.lemmatize(word) for word in document_test]
        document_test = ' '.join(document_test)
        documents_clean+=(document_test)
    
    return documents_clean

def wordcloud(clean_text):
    image=wc.st_ui(clean_text).value
    return image
    


def pdf_extract():
    st.set_page_config(layout = "wide")
    st.title("PDF data extraction")

    
    fileupload = st.sidebar.file_uploader("Upload a PDF document here")

    if fileupload:
        pdfbytes = fileupload.getvalue()
        doc = return_doc_from_bytes(pdfbytes)  
        text = ''
        for page in doc:
            text += page.get_text()
        sentences = nltk.sent_tokenize(text)
        clean_text=preprocessing(sentences)
        #st.write(clean_text)
        image=wordcloud(clean_text)
        st.header("WordCloud !")
        st.image(image)
        

if __name__ == "__main__":
    pdf_extract()
    
