import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Function to preprocess text data
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenization
    tokenizer = nltk.tokenize.WhitespaceTokenizer()
    tokens = tokenizer.tokenize(text)
    
    # Remove stopwords
    default_stopwords = set(stopwords.words('english'))

    # Words to remove from the stopwords list
    words_to_keep = {'how', 'when', 'where','what','who','why','before','during','after'}

    # Customize stopwords by removing specific words
    final_stopwords = default_stopwords - words_to_keep

    filtered_tokens = [word for word in tokens if word not in final_stopwords]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    
    # Join tokens back into text
    preprocessed_text = ' '.join(lemmatized_tokens)
    
    return preprocessed_text


def load_job_data(file_path):
    job_data = pd.read_csv(file_path)

    return job_data

def preprocess_job_data(file_path):
    job_data = pd.read_csv(file_path)

    # Drop rows with NaN values in the 'summary' column
    job_data = job_data.dropna(subset=['summary'])

    # Data preprocessing
    job_data['summary'] = job_data['summary'].apply(preprocess_text)
    job_data['location'] = job_data['location'].apply(preprocess_text)

    
    # Convert 'num_ratings' to integer
    job_data['num_ratings'] = job_data['num_ratings'].fillna(0).astype(int)
    
    return job_data

def load_events(file_path):
    job_data = pd.read_csv(file_path)

    return job_data

def save_preprocessed_data(input_file_path, output_file_path):
    preprocessed_job_data = preprocess_job_data(input_file_path)
    preprocessed_job_data.to_csv(output_file_path, index=False)
    print(f"Preprocessed data saved to {output_file_path}")

def main():
    input_file_path = 'dataset/job_data.csv'  # Path to your input CSV file
    output_file_path = 'dataset/preprocessed_job_data.csv'  # Path to save the preprocessed CSV file

    save_preprocessed_data(input_file_path, output_file_path)

if __name__ == "__main__":
    main()
