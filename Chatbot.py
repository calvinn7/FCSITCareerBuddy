import pandas as pd
import streamlit as st
import nltk
import re
import spacy
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Load English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# Load CSV data
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

# Spell Check word
def spell_check(token_words, job_location,job_company):
    spell = SpellChecker()
    known_terms = ['sql', 'java', 'python', 'c++']
    job_location_lower = []
    job_company_lower=[]

    for location in job_location:
        words = tokenization(location)
        for word in words:
            if '/' in word:
                split_words = word.split('/')
                job_location_lower.extend(split_words)
            else:
                job_location_lower.append(word)

    for company in job_company:
        c_name = tokenization(company)
        for name in c_name:
            if '.' in name:
                split_name = name.split('.')
                job_company_lower.extend(split_name)
            else:
                job_company_lower.append(name)
    


    known_terms.extend(job_location_lower)
    known_terms.extend(job_company_lower)
    
    corrections = {}
    for word in token_words:
        if word in known_terms:
            corrections[word] = word
        else:
            correction = spell.correction(word)
            if correction is not None:
                corrections[word] = correction
            else:
                corrections[word] = word 
    corrected_sentence = " ".join(corrections.values())
    return corrected_sentence
 


# Stopword Removal
def stop_remove(lem_sent):
    doc = nlp(lem_sent)
    filtered_words = [token.text for token in doc if not token.is_stop]
    clean_text = ' '.join(filtered_words)
    return clean_text

# Lemmatization of sentence
def lemmatize_sentence(corrected_sentence, job_location):
    doc = nlp(corrected_sentence)
    lemmatized_words = []
    job_location_lower = [location.lower() for location in job_location]
    for token in doc:
        if token.text.lower() in job_location_lower:
            lemmatized_words.append(token.text)
        else:
            lemmatized_words.append(token.lemma_)
    clean_text = ' '.join(lemmatized_words)
    return clean_text


def recommend_jobs(user_input, job_data):
    # Combine job titles and descriptions into a single text representation
    job_text = job_data['JobTitle'] + ' ' + job_data['summary'] + ' ' + job_data['company'] + ' ' + job_data['location']


    # Vectorize combined text using TF-IDF
    vectorizer = TfidfVectorizer(max_df=0.8, min_df=2)
    X_train_vectorized = vectorizer.fit_transform(job_text)

    # Vectorize user input
    input_vector = vectorizer.transform([user_input])

    # Calculate cosine similarity between user input and job titles/descriptions
    similarities = cosine_similarity(input_vector, X_train_vectorized)

    # Get indices sorted by similarity
    indices = similarities.argsort(axis=1)[0][-5:][::-1]

    # Filter jobs based on similarity
    recommended_jobs = job_data.iloc[indices]

    return recommended_jobs



def main():
    st.title("Job Recommendation")
    user_input = st.text_input(label="", placeholder="Ask your job preferences")
    search_button = st.button("Search")  



    if search_button and user_input:

        df = load_csv()

        job_location=df['location'].unique()
        job_salary=df['salary'].unique()
        job_company=df['company'].unique()

        token_words = tokenization(user_input)
        corrected_sentence = spell_check(token_words,job_location,job_company)
        st.write("Spell Check: ",corrected_sentence)
        remove_word = stop_remove(corrected_sentence)
        st.write("Stop Word: ",remove_word)
        user_process_sentence = lemmatize_sentence(remove_word,job_location)
        st.write("Preprocessed Text:", user_process_sentence)
        


        # Recommend jobs based on user input
        recommended_jobs = recommend_jobs(user_process_sentence, df)
        
        # Display recommended jobs
        st.subheader("Recommended Jobs:")
        st.dataframe(recommended_jobs)

if __name__ == "__main__":
    main()