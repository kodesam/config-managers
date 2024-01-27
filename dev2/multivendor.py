import tensorflow as tf
from transformers import TFLongformerForSequenceClassification, LongformerTokenizer
import streamlit as st
import tensorflow as tf

# Check TensorFlow version
st.write("TensorFlow version:", tf.__version__)

# Rest of your Streamlit app code goes here...

# Load the tokenizer
tokenizer = LongformerTokenizer.from_pretrained('tokenizer_directory')

# Load the pre-trained LLM model
model = TFLongformerForSequenceClassification.from_pretrained('llm_model_directory')

# Input your intent
intent = "Your input intent goes here"

# Tokenize the intent
inputs = tokenizer.encode_plus(intent, padding="longest", truncation=True, return_tensors="tf")

# Generate response
outputs = model(inputs["input_ids"])

# Get predicted response class
pred_class = tf.argmax(outputs.logits, axis=1).numpy()[0]

# Get response using predicted class
response = model.config.id2label[pred_class]

print("Response:", response)