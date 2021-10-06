from tensorflow.keras.models import load_model
import numpy as np

model_path = "/Users/vaibhavsatpathy/Documents/products/aikosh/text_processing/text_classification/models_v2"

model = load_model(model_path)

sample_text = "I went on a successful data and was really happy post that."
test_input = np.asarray([sample_text])
response = model.predict(test_input)
print(response)
