from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

# Download necessary resources for NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def faq_preprocess_text(text):
    text = text.lower()
    # Tokenization
    tokens = word_tokenize(text)
    
    # Removing punctuation
    tokens = [token for token in tokens if token not in string.punctuation]
    
    # Get the default stopwords list
    default_stopwords = set(stopwords.words('english'))

    # Words to remove from the stopwords list
    words_to_keep = {'how', 'when', 'where','what','who','why','before','during','after'}

    # Customize stopwords by removing specific words
    final_stopwords = default_stopwords - words_to_keep

        # Removing stopwords
    tokens = [token for token in tokens if token not in final_stopwords]
    
    # Initialize lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatization
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]  # Apply lower() to each token
    
    # Join tokens back into a single string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text


vectorizer = TfidfVectorizer()

def get_most_similar_question(input_question, threshold=0.001):
    # Load the CSV file
    qa_df = pd.read_csv('dataset/faq_data.csv')
    qa_df['question'] = qa_df['question'].apply(faq_preprocess_text)


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