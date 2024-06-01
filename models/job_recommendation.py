import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD, NMF
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def recommend_jobs(user_input, job_data):

    # Combine job titles and descriptions into a single text representation
    job_text = job_data['JobTitle'] + ' ' + job_data['summary'] + ' ' 
    + job_data['company'] + ' ' + job_data['location'] + ' ' + job_data['salary']

    model = 'lsa'

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

