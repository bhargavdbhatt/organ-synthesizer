import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import requests
import os

# Disable SSL verification
os.environ['CURL_CA_BUNDLE'] = ''
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


# Load the tokenizer and model for sequence classification
tokenizer = AutoTokenizer.from_pretrained("huawei-noah/TinyBERT_General_4L_312D" , use_auth_token=False, trust_remote_code=True)
model = AutoModelForSequenceClassification.from_pretrained("huawei-noah/TinyBERT_General_4L_312D", num_labels=2 , use_auth_token=False, trust_remote_code=True)

# Example input text
text = "TinyBERT is a smaller version of BERT."

# Tokenize the input text
inputs = tokenizer(text, return_tensors="pt")

# Run the model and get the logits
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits

# Get the predicted class
predicted_class = torch.argmax(logits, dim=1).item()

print(f"Predicted class: {predicted_class}")