from silence_tensorflow import silence_tensorflow
silence_tensorflow()

import tensorflow as tf
from transformers import TFBertForSequenceClassification, BertTokenizer,logging
from django.conf import settings
logging.set_verbosity_error()

def predict_text(text):
    tokenizer = BertTokenizer.from_pretrained(f"{settings.BASE_DIR}/model/ai_human_classifier")                      # -> tokenizer
    model = TFBertForSequenceClassification.from_pretrained(f"{settings.BASE_DIR}/model/ai_human_classifier")         # -> model  
    encoding = tokenizer(
        text,
        return_tensors="tf",
        max_length=256,
        truncation=True,
        padding="max_length"
    )
    
    logits = model(encoding).logits
    predicted_probs = tf.nn.softmax(logits, axis=-1).numpy()[0]
    predicted_class = tf.argmax(predicted_probs).numpy() 
    
    probabilities_percentage = [round(prob * 100, 2) for prob in predicted_probs]
    
    return {
    "prediction": "AI-generated" if predicted_class == 0 else "Human-generated",
    "accuracy": round(float(probabilities_percentage[0]),2) if predicted_class == 0 else round(float(probabilities_percentage[1]),2)
    }

# Example usage
# new_text = "This is grate to hear."
# prediction = predict_text(new_text)
# print(prediction)