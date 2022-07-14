from tensorflow.keras import Model
from tensorflow.keras.layers import Conv1D, Bidirectional, LSTM, Dense
from tensorflow.keras.utils import plot_model
from tensorflow.keras import Sequential
import tensorflow.keras.backend as K
import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import GRU
from tensorflow.keras.layers import Dropout


class AttentionLayer(Layer):

    def __init__(self, units):
        super(AttentionLayer, self).__init__()
        self.W = Dense(units, kernel_initializer='he_normal')
        self.V = Dense(1, kernel_initializer='he_normal')

    def call(self, encoder_output, **kwargs):
        score = self.V(K.tanh(self.W(encoder_output)))

        attention_weights = K.softmax(score, axis=1)

        context_vector = attention_weights * encoder_output
        context_vector = tf.reduce_sum(context_vector, axis=1)
        return context_vector

    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'W': self.W,
            'V': self.V,
        })
        return config


class GRU_Attention(Model):
    def __init__(self, sequence_length):
        super(GRU_Attention, self).__init__()

        self.model = Sequential()
        # 卷积层1
        self.model.add(Conv1D(16, 4, activation='relu', input_shape=(sequence_length, 1), padding="same", strides=1))
        # 两层双向GRU
        self.model.add(Bidirectional(GRU(64, activation='relu', return_sequences=True), merge_mode='concat'))
        self.model.add(Dropout(0.5))
        self.model.add(Bidirectional(GRU(128, activation='relu', return_sequences=False), merge_mode='concat'))
        self.model.add(Dropout(0.5))
        # self.model.add(AttentionLayer(units=128))
        # 全连接层
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1, activation='linear'))
        self.model.compile(loss='mse', optimizer='adam')

    def call(self, inputs, raining=None, mask=None):
        return self.model(inputs)
