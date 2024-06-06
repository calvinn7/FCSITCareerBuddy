import torch
import pickle
from transformers import BertTokenizer, BertForSequenceClassification

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