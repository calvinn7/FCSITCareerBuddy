import pandas as pd
import streamlit as st
import nltk
import re
import spacy
from textblob import TextBlob 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD, NMF


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")


def load_csv():
    df = pd.read_csv("C:/Users/ASUS/OneDrive/Desktop/NLP/src/dataset/job_data.csv") 
    return df

# Tokenization of user input
def tokenization(user_input):
    user_input = user_input.lower() 
    user_input = re.sub(r'[().?]', '', user_input)
    tokenizer = nltk.tokenize.WhitespaceTokenizer()
    token_words = tokenizer.tokenize(user_input)
    return token_words 

# Spell Check word using pyspellchecker
def spell_check(token_words, job_location, job_company):
    known_terms = {'sql', 'java', 'python', 'c++','backend','frontend','intern','rm','php'}  
    job_location_lower = set()
    job_company_lower = set()

    for location in job_location:
        words = tokenization(location)
        for word in words:
            if '/' in word:
                split_words = word.split('/')
                job_location_lower.update(split_words)
            else:
                job_location_lower.add(word)

    for company in job_company:
        c_name = tokenization(company)
        for name in c_name:
            if '.' in name:
                split_name = name.split('.')
                job_company_lower.update(split_name)
            else:
                job_company_lower.add(name)

    known_terms.update(job_location_lower)
    known_terms.update(job_company_lower)

    specific_corrections = {
        'interns': 'intern',
    }

    corrections = {}
    for word in token_words:
        if word in specific_corrections:
            corrections[word] = specific_corrections[word]
        elif word in known_terms:
            corrections[word] = word
        else:
            correction = TextBlob(word).correct()
            corrections[word] = str(correction)
                
    corrected_sentence = " ".join(corrections.values())
    return corrected_sentence

# Stopword Removal
def stop_remove(lem_sent):
    custom_stopwords = {'front', 'back'} 
    doc = nlp(lem_sent)
    filtered_words = [token.text for token in doc if not token.is_stop or token.text in custom_stopwords]
    clean_text = ' '.join(filtered_words)
    return clean_text

# Lemmatization of sentence
def lemmatize_sentence(corrected_sentence, job_location, job_company):
    doc = nlp(corrected_sentence)
    lemmatized_words = []
    job_location_lower = [location.lower() for location in job_location]
    job_company_lower = [company.lower() for company in job_company]
    for token in doc:
        if token.text.lower() in job_location_lower or token.text.lower() in job_company_lower:
            lemmatized_words.append(token.text)
        else:
            lemmatized_words.append(token.lemma_)
    clean_text = ' '.join(lemmatized_words)
    return clean_text



def recommend_jobs(user_input, job_data, model):

    #For now i use lsa model
    job_text = job_data['JobTitle'] + ' ' + job_data['summary'] + ' ' + job_data['company'] + ' ' + job_data['location'] + ' ' + job_data['salary']

    if model == 'cosine_similarity':
        vectorizer = TfidfVectorizer(max_df=0.8, min_df=2)
        X_train_vectorized = vectorizer.fit_transform(job_text)
        input_vector = vectorizer.transform([user_input])
        similarities = cosine_similarity(input_vector, X_train_vectorized)
        indices = similarities.argsort(axis=1)[0][-5:][::-1]
        recommended_jobs = job_data.iloc[indices]
        return recommended_jobs
    
    
    elif model == 'lsa':
        vectorizer = TfidfVectorizer(max_df=0.8, min_df=2)
        svd = TruncatedSVD(n_components=100, random_state=42)
        lsa = make_pipeline(vectorizer, svd, Normalizer(copy=False))
        X_train_lsa = lsa.fit_transform(job_text)
        input_lsa = lsa.transform([user_input])
        similarities = cosine_similarity(input_lsa, X_train_lsa)
        indices = similarities.argsort(axis=1)[0][-5:][::-1]
        recommended_jobs = job_data.iloc[indices]
        return recommended_jobs
    
    
    else:
        raise ValueError("Invalid model type. Please choose from 'cosine_similarity' or 'lsa'.")
    
def main():
    st.title("Job Recommendation")
    user_input = st.text_input(label="", placeholder="Enter your job preferences")
    

    #Change according to preference
    model='lsa'
    
    search_button = st.button("Search")  

    if search_button and user_input:
        df = load_csv()
        job_location = df['location'].unique()
        job_salary = df['salary'].unique()
        job_company = df['company'].unique()

        token_words = tokenization(user_input)
        corrected_sentence = spell_check(token_words, job_location, job_company)
        st.write("Spell Check: ", corrected_sentence)
        remove_word = stop_remove(corrected_sentence)
        st.write("Stop Word: ", remove_word)
        user_process_sentence = lemmatize_sentence(remove_word, job_location,job_company)
        st.write("Preprocessed Text:", user_process_sentence)

        recommended_jobs = recommend_jobs(user_process_sentence, df, model=model)
        
        st.subheader("Recommended Jobs:")
        st.dataframe(recommended_jobs)

if __name__ == "__main__":
    main()
