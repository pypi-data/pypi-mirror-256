from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Dropout, Activation,BatchNormalization,GaussianNoise
from keras.optimizers import SGD,RMSprop,Adam
from tensorflow.keras.layers import LeakyReLU,Reshape
import keras_tuner as kt
import tensorflow as tf
from utils import layers
import keras.optimizers as opt
import numpy as np

def train(X_train,n1,n2,n3,n4,batch_size,n_epochs,learningrate,activation,optimizer):
    
    if learningrate is None:
        optimizer = opt.__dict__[optimizer]()
    else:
        optimizer = opt.__dict__[optimizer](lr=learningrate)
    # Build and compile the discriminator
    discriminator = layers.build_discriminator(n1,n2,n3,n4,activation)
    discriminator.compile(loss='binary_crossentropy',
        optimizer=optimizer,
        metrics=['accuracy'])

    # Build the encoder / decoder
    encoder = layers.build_encoder(n1,n2,n3,n4,activation)
    decoder = layers.build_decoder(n1,n2,n3,n4,activation)

    autoencoder_input = Input(shape=(n1,))
    reconstructed_input = Input(shape=(n1,))
        # The generator takes the image, encodes it and reconstructs it
        # from the encoding
    encoded_repr = encoder(autoencoder_input)
    reconstructed = decoder(encoded_repr)

    # For the adversarial_autoencoder model we will only train the generator
    discriminator.trainable = False

    # The discriminator determines validity of the encoding
    validity = discriminator(encoded_repr)

    # The adversarial_autoencoder model  (stacked generator and discriminator)
    adversarial_autoencoder = Model(autoencoder_input, [reconstructed, validity])
    adversarial_autoencoder.compile(loss=['mse', 'binary_crossentropy'],
            loss_weights=[0.999, 0.001],
            optimizer=optimizer)

    valid = np.ones((batch_size, 1))
    fake = np.zeros((batch_size, 1))

    for epoch in np.arange(1, n_epochs + 1):
        for i in range(int(len(X_train) / batch_size)):

            # ---------------------
            #  Train Discriminator
            # ---------------------

            # Select a random batch of images
            batch = X_train[i*batch_size:i*batch_size+batch_size]

    
            latent_fake = encoder.predict(batch)
            latent_real = np.random.normal(size=(batch_size, n4))

            # Train the discriminator
            d_loss_real = discriminator.train_on_batch(latent_real, valid)
            d_loss_fake = discriminator.train_on_batch(latent_fake, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

                # ---------------------
                #  Train Generator
                # ---------------------

                # Train the generator
            g_loss = adversarial_autoencoder.train_on_batch(batch, [batch, valid])

            # Plot the progress
        print ("%d [D loss: %f, acc: %.2f%%] [G loss: %f, mse: %f]" % (epoch, d_loss[0], 100*d_loss[1], g_loss[0], g_loss[1]))

    return adversarial_autoencoder