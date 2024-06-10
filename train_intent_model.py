import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
import pickle
import logging
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from data_preprocessing import preprocess_text

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load data from CSV
logger.info("Loading data from CSV...")
intent_data = pd.read_csv('dataset\\intent_data.csv')

# Preprocess the text data
logger.info("Preprocessing text data...")
intent_data['query'] = intent_data['query'].apply(preprocess_text)

# Encode labels
logger.info("Encoding labels...")
le = LabelEncoder()
intent_data['intent'] = le.fit_transform(intent_data['intent'])

# Save the label encoder
with open('models/label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)
logger.info("Label encoder saved to 'label_encoder.pkl'")

# Train-test split
logger.info("Splitting data into train and validation sets...")
train_texts, val_texts, train_labels, val_labels = train_test_split(intent_data['query'], intent_data['intent'], test_size=0.3)

# Load tokenizer
logger.info("Loading tokenizer...")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize data
logger.info("Tokenizing data...")
train_encodings = tokenizer(train_texts.tolist(), truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts.tolist(), truncation=True, padding=True, max_length=128)

# Convert labels to tensors
train_labels = torch.tensor(train_labels.tolist())
val_labels = torch.tensor(val_labels.tolist())

# Create a Dataset class
class IntentDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

# Create datasets
logger.info("Creating datasets...")
train_dataset = IntentDataset(train_encodings, train_labels)
val_dataset = IntentDataset(val_encodings, val_labels)

# Load model
logger.info("Loading model...")
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(le.classes_))

# Training arguments
logger.info("Setting up training arguments...")
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=10,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=170,
    weight_decay=0.0193,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True
)

# Trainer
logger.info("Setting up Trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# Train the model
logger.info("Starting training...")
trainer.train()

# Save the model and tokenizer
logger.info("Saving model and tokenizer...")
model.save_pretrained('./models/intent_model')
tokenizer.save_pretrained('./models/intent_model')

# Save training arguments
with open('./models/intent_model/training_args.bin', 'wb') as f:
    pickle.dump(training_args, f)
logger.info("Training arguments saved to './models/intent_model/training_args.bin'")

# Evaluate the model
logger.info("Evaluating the model...")
eval_results = trainer.evaluate()
logger.info(f"Evaluation results: {eval_results}")

# Additional evaluation metrics
# Prediction and labels for validation set
val_preds = trainer.predict(val_dataset)

# Get the predicted labels
pred_labels = torch.argmax(torch.tensor(val_preds.predictions), axis=1)

# Calculate accuracy, precision, recall, and F1 score
accuracy = accuracy_score(val_labels, pred_labels)
precision, recall, f1, _ = precision_recall_fscore_support(val_labels, pred_labels, average='weighted')

# Log the results
logger.info(f"Validation Accuracy: {accuracy:.4f}")
logger.info(f"Validation Precision: {precision:.4f}")
logger.info(f"Validation Recall: {recall:.4f}")
logger.info(f"Validation F1 Score: {f1:.4f}")