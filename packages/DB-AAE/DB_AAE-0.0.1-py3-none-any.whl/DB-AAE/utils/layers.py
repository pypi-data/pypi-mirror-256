from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Dropout, Activation,BatchNormalization,GaussianNoise
from keras.optimizers import SGD,RMSprop,Adam,Adagrad
from tensorflow.keras.layers import LeakyReLU,Reshape
import tensorflow as tf
import numpy as np

def build_encoder(n1, n2, n3, n4, activation):
    # Encoder

    expr_in = Input(shape=(n1,))

    h = Dense(n2)(expr_in)
    h = LeakyReLU(alpha=0.2)(h)
    h = Dense(n3)(h)
    h = LeakyReLU(alpha=0.2)(h)
    mu = Dense(n4)(h)
    log_var = Dense(n4)(h)
    latent_repr = tf.keras.layers.Add()([mu, log_var])

    return Model(expr_in, latent_repr)


def build_decoder(n1,n2,n3,n4,activation):
    model = Sequential()

    model.add(Dense(n3, input_dim=n4))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(n2))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(np.prod((n1,)), activation='relu'))
    model.add(Reshape((n1,)))

    model.summary()

    z = Input(shape=(n4,))
    expr_lat = model(z)

    return Model(z, expr_lat)

def build_discriminator(n1,n2,n3,n4,activation):
    model = Sequential()

    model.add(Dense(n3, input_dim=n4))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(256))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(1, activation="relu"))
    model.summary()

    encoded_repr = Input(shape=(n4,))
    validity = model(encoded_repr)

    return Model(encoded_repr, validity)


