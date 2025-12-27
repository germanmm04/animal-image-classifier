import tensorflow as tf

class Classifier:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, input_array):
        return self.model.predict(input_array)
