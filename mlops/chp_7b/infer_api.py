import uvicorn
import numpy as np
import json

from fastapi import FastAPI
from tensorflow.keras.models import load_model

# Give local path to your models and labels
# Add the model to your folder to package it accurately and use it
model_path = "/app/models_v2"
labels_path = "/app/labels.json"

# Read the labels
with open(labels_path, "r") as f:
    labels = json.load(f)

# Load your model and create its instance
model = load_model(model_path)

# Declare a FastAPI instance
app = FastAPI()


# Create a POST type of router with a URL end point name of your choice
# Your POST request carries the text in its query
@app.post("/test_model")
async def test_function(sample_text: str):

    # Read the Text and convert it into a numpy array
    test_input = np.asarray([sample_text])

    # Send your Text for Prediction and receive a numpy array of probabilities
    prediction = model.predict(test_input)

    # Read the corresponding label from your Labels JSON
    index = np.argmax(prediction)
    predicted_label = labels.get(str(index))

    # Return the predicted Label
    return {"Prediction": predicted_label}


# Run the script
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
