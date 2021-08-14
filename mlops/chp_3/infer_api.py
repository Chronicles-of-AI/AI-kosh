import uvicorn
import io
import numpy as np
import json

from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from PIL import Image

# Give local path to your models and labels
model_path = "/app/model_intel.h5"
labels_path = "/app/labels.json"

# Read the labels
with open(labels_path, "r") as f:
    labels = json.load(f)

# Load your model and create its instance
model = load_model(model_path)

# Declare a FastAPI instance
app = FastAPI()

# Create a POST type of router with a URL end point name of your choice
# Add Uploadfile to your API so that you can upload images to test
@app.post("/test_model")
async def test_function(file: UploadFile = File(...)):
    # Read file in bytes format
    file_content = await file.read()

    # Convert Bytes file into an Image of Numpy array format and
    # Resize it to the size as expected by your model in training
    image = np.asarray(Image.open(io.BytesIO(file_content)).resize((100, 100)))
    image = np.expand_dims(image, axis=0)
    image = np.divide(image, 255.0)

    # Send your Image for Prediction and receive a numpy array of probabilities
    prediction = model.predict(image)

    # Read the corresponding label from your Labels JSON
    index = np.argmax(prediction)
    predicted_label = labels.get(str(index))

    # Return the predicted Label
    return {"Prediction": predicted_label}


# Run the script
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
