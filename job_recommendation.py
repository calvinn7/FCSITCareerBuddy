from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_jobs(user_input, job_data):
 
    # Feature extraction using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8, min_df=2)
    X_train_vectorized = vectorizer.fit_transform(job_data['summary'])
    
    # Convert user input to feature vector
    input_vector = vectorizer.transform([user_input])
    
    # Calculate cosine similarity between user input and job descriptions
    similarities = cosine_similarity(input_vector, X_train_vectorized)
    
    # Sort jobs by similarity and recommend the top 5 most similar jobs
    top_indices = similarities.argsort(axis=1)[0][-5:][::-1]  # Get indices of top 5 most similar jobs
    recommended_jobs = job_data.iloc[top_indices]
    
    return recommended_jobs
