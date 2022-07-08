from tensorflow.keras import Model
from tensorflow.keras.layers import Conv1D, Dense, Dropout, Flatten
from tensorflow.keras.models import Sequential


class Seq2Point(Model):

    def __init__(self, sequence_length):
        super(Seq2Point, self).__init__()
        self.model = Sequential()
        self.model.add(Conv1D(30, 10, activation="relu", input_shape=(sequence_length, 1), strides=1))
        self.model.add(Conv1D(30, 8, activation='relu', strides=1))
        self.model.add(Conv1D(40, 6, activation='relu', strides=1))
        self.model.add(Conv1D(50, 5, activation='relu', strides=1))
        self.model.add(Dropout(.2))
        self.model.add(Conv1D(50, 5, activation='relu', strides=1))
        self.model.add(Dropout(.2))
        self.model.add(Flatten())
        self.model.add(Dense(1024, activation='relu'))
        self.model.add(Dropout(.2))
        self.model.add(Dense(1))

    def call(self, inputs, training=None, mask=None):
        return self.model(inputs)