import pandas as pd
import random
import numpy as np
import os
import json

import tensorflow as tf
import tensorflow_hub as hub


def data_loader(bs, data, y_lab):
    while True:
        texts = []
        labels = []
        while len(texts) < bs:
            indice = random.randint(0, len(data) - 1)
            target = data[indice][1]
            labels.append(y_lab[target])

            test_text = data[indice][0]
            texts.append(test_text)

        yield np.asarray(texts), np.asarray(labels)


def model_arc(y_labels):
    embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
    hub_layer = hub.KerasLayer(
        embedding, input_shape=[], dtype=tf.string, trainable=True
    )
    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(16, activation="relu"))
    model.add(tf.keras.layers.Dense(len(y_labels), activation="softmax"))

    model.summary()
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def data_reader(dataset_path: str):
    data = pd.read_csv(dataset_path)
    all_labels = {}
    all_text = []

    for index, row in data.iterrows():
        text = row[0]
        label = row[1]
        all_text.append((text, label))
        if label not in all_labels:
            all_labels[label] = len(all_labels)

    rev_labels = {}
    for key, labels in all_labels.items():
        rev_labels[labels] = key

    return all_text, all_labels, rev_labels


def train(dataset_path, batch_size, epochs):
    all_text, all_labels, rev_labels = data_reader(dataset_path=dataset_path)

    print("target_encodings: ", all_labels)
    print("Number of training texts: ", len(all_text))

    with open(os.path.join(output_dir, "labels.json"), "w") as f:
        json.dump(rev_labels, f)

    train_generator = data_loader(bs=batch_size, y_lab=all_labels, data=all_text)

    model = model_arc(y_labels=all_labels)

    model.fit_generator(
        generator=train_generator,
        steps_per_epoch=(len(all_text) // batch_size),
        epochs=epochs,
    )
    tf.keras.models.save_model(model, filepath=os.path.join(output_dir, "models_v2"))


dataset_path = (
    "/Users/vaibhavsatpathy/Documents/pocs/automl_nl_data/NL-classification.csv"
)

output_dir = "/Users/vaibhavsatpathy/Documents/products/aikosh/text_processing/text_classification/"
batch_size = 8
epochs = 3
train(
    dataset_path=dataset_path,
    batch_size=batch_size,
    epochs=epochs,
)
