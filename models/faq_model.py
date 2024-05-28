from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from data_preprocessing import preprocess_text


vectorizer = TfidfVectorizer()


def get_most_similar_question(input_question, threshold=0.001):
    # Load the CSV file
    qa_df = pd.read_csv('dataset/faq_data.csv')
    qa_df['question'] = qa_df['question'].apply(preprocess_text)


    # Vectorize the questions in the dataset
    tfidf_matrix = vectorizer.fit_transform(qa_df['question'])

    # Vectorize the input question
    input_vector = vectorizer.transform([input_question])
    
    # Calculate cosine similarity
    similarities = cosine_similarity(input_vector, tfidf_matrix)
    
    # Get the index of the most similar question
    most_similar_index = similarities.argmax()
    most_similar_score = similarities[0, most_similar_index]
    
    if most_similar_score < threshold:
        return {
            "answer": "Sorry, the answer to that question is not available in the data. Please ask your internship coordinator for the answer.",
            "question": ""
        }
    
    return qa_df.iloc[most_similar_index]