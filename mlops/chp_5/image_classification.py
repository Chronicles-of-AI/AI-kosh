import os
import random
import numpy as np
import mlflow

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.layers import Input, Conv2D, Flatten, Dense
from tensorflow.keras.models import Model


def data_loader(bs, data, y_lab, image_input_shape):
    while True:
        images = []
        labels = []
        while len(images) < bs:
            indice = random.randint(0, len(data) - 1)
            target = data[indice].split("/")[-2]
            labels.append(y_lab[target])

            test_img = np.asarray(load_img(data[indice], target_size=image_input_shape))
            img = np.divide(test_img, 255.0)
            images.append(img)

        yield np.asarray(images), np.asarray(labels)


def model_arc(y_labels, image_inp_shape):
    inp_layer_images = Input(shape=image_inp_shape)

    conv_layer = Conv2D(filters=64, kernel_size=(2, 2), activation="relu")(
        inp_layer_images
    )
    flatten_layer = Flatten()(conv_layer)
    out_layer = Dense(len(y_labels), activation="softmax")(flatten_layer)
    model = Model(inp_layer_images, out_layer)
    model.summary()
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def data_reading(dataset_path):
    all_labels = {}
    all_images = []
    for folders in os.listdir(dataset_path):
        if folders != ".DS_Store":
            folder_path = os.path.join(dataset_path, folders)
            all_labels[folders] = len(all_labels)
            for images in os.listdir(folder_path):
                if images != ".DS_Store":
                    image_path = os.path.join(folder_path, images)
                    all_images.append(image_path)

    rev_labels = {}
    for key, labels in all_labels.items():
        rev_labels[labels] = key

    return all_images, all_labels, rev_labels


def train(dataset_path, batch_size, epochs, input_shape):
    with mlflow.start_run():
        all_images, all_labels, rev_labels = data_reading(dataset_path=dataset_path)

        print("target_encodings: ", all_labels)
        print("Number of training images: ", len(all_images))

        params = {
            "batch_size": batch_size,
            "epochs": epochs,
            "input_shape": input_shape,
            "encodings": all_labels,
            "training_images": len(all_images),
        }
        mlflow.log_params(params)

        train_generator = data_loader(
            bs=batch_size,
            y_lab=all_labels,
            image_input_shape=input_shape,
            data=all_images,
        )

        model = model_arc(y_labels=all_labels, image_inp_shape=input_shape)

        history = model.fit_generator(
            generator=train_generator,
            steps_per_epoch=(len(all_images) // batch_size),
            epochs=epochs,
        )
        model.save("image_classification_model.h5")
        accuracy = history.history.get("accuracy")
        loss = history.history.get("loss")
        for index, value in enumerate(accuracy):
            mlflow.log_metric(key="accuracy", value=value, step=index)
        for index, value in enumerate(loss):
            mlflow.log_metric(key="loss", value=value, step=index)
        mlflow.end_run()


experiment_name = "image_classification"
s3_artifacts_path = "s3://mlops-manifest-files/mlflow"
experiment = mlflow.get_experiment_by_name(name=experiment_name)
if experiment:
    pass
else:
    experiment = mlflow.create_experiment(
        name=experiment_name,
        artifact_location=s3_artifacts_path,
    )
mlflow.set_experiment(experiment_name=experiment_name)
mlflow.tensorflow.autolog()
dataset_path = "/Users/vsatpathy/Desktop/off_POCs/intel-image-classification/seg_train/"
batch_size = 16
epochs = 2
input_shape = (100, 100, 3)
train(
    dataset_path=dataset_path,
    batch_size=batch_size,
    epochs=epochs,
    input_shape=input_shape,
)
