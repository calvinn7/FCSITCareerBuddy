import torch
import pickle
from transformers import BertTokenizer, BertForSequenceClassification
from data_preprocessing import preprocess_text


# Load the saved model and tokenizer
model = BertForSequenceClassification.from_pretrained('./models/intent_model')
tokenizer = BertTokenizer.from_pretrained('./models/intent_model')

# Load the label encoder
with open('./models/label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

# Define a confidence threshold
CONFIDENCE_THRESHOLD = 0.5

def classify_intent(query):
    inputs = tokenizer(query, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    # Get the highest confidence score and its corresponding class
    max_prob, predicted_class = torch.max(probs, dim=1)
    
    # Check if the highest confidence score is below the threshold
    if max_prob.item() < CONFIDENCE_THRESHOLD:
        return None

    predicted_class = torch.argmax(probs, dim=1).item()
    return le.inverse_transform([predicted_class])[0]
"""
# Test cases
test_queries = [
    "How to apply for internship?",
    "Can you tell me about upcoming networking events?",
    "Is there a workshop on data science?",
    "I want to know more Data Analyst jobs."
]

# Testing the function
print("Testing intent classification:\n")
for query in test_queries:
    intent = classify_intent(preprocess_text(query))
    if intent is not None:
        print(f"Query: {query}\nPredicted Intent: {intent}\n")
    else:
        print(f"Query: {query}\nPredicted Intent: Not confident enough to classify\n")
"""
