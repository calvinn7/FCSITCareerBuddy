import torch
import pickle
from transformers import BertTokenizer, BertForSequenceClassification

# Load the saved model and tokenizer
model = BertForSequenceClassification.from_pretrained('./models/intent_model')
tokenizer = BertTokenizer.from_pretrained('./models/intent_model')

# Load the label encoder
with open('./models/label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

def classify_intent(query):
    inputs = tokenizer(query, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(probs, dim=1).item()
    return le.inverse_transform([predicted_class])[0]