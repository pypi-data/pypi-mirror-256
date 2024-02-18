from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Dropout, Activation,BatchNormalization,GaussianNoise
from keras.optimizers import SGD,RMSprop,Adam
from tensorflow.keras.layers import LeakyReLU,Reshape
import keras_tuner as kt
import tensorflow as tf
import keras.optimizers as opt
from utils import layers
import numpy as np

class AEHyperModel(kt.HyperModel):
    def __init__(self,X_train,n1,n2,n3,n4,hyperepoch,learningrate,activation,optimizer):
        self.X_train=X_train
        self.n1 = n1
        self.n2 = n2
        self.n3= n3
        self.n4= n4
        self.learningrate=learningrate
        self.activation=activation
        self.optimizer=optimizer
        self.hyperepoch=hyperepoch
    # def create_discriminator(n1,n2,n3,n4,activation,learning_rate):

    #  return discriminator
    
    def build(self, hp):
        hp_n2 = hp.Int('units_2', min_value=512, max_value=1024, step=32)
        hp_n3 = hp.Int('units_3', min_value=32, max_value=512, step=32)
        hp_n3 = hp.Int('units_3', min_value=512, max_value=1024, step=32)
        hp_n4 = hp.Int('units_4', min_value=32, max_value=512, step=32)
        # encoder=keras_3layer_encoder(n1,hp_n2,hp_n3,activation)
        # decoder=keras_3layer_decoder(n1,hp_n2,hp_n3,activation)
        # encoder=keras_4layer_encoder(n1,hp_n2,hp_n3,hp_n4,activation)
        # decoder=keras_4layer_decoder(n1,hp_n2,hp_n3,hp_n4,activation)
        # Build the encoder / decoder
        encoder = layers.build_encoder(self.n1, self.n2, self.n3, self.n4, self.activation)
        decoder = layers.build_decoder(self.n1, self.n2, self.n3, self.n4, self.activation)
        # Build and compile the discriminator
        ##discriminator = build_discriminator(n1,n2,n3,n4,activation)
        #optimizer = RMSprop(learning_rate=0.00002)
        if self.learningrate is None:
            optimizer = opt.__dict__[self.optimizer]()
        else:
            optimizer = opt.__dict__[self.optimizer](lr=self.learningrate)
        ##discriminator.compile(loss='binary_crossentropy',optimizer=optimizer,metrics=['accuracy'])
        # autoencoder_input = Input(shape=(n1,))
        # autoencoder = Model(autoencoder_input, decoder(encoder(autoencoder_input)))
        discriminator = layers.build_discriminator(self.n1, self.n2, self.n3, self.n4, self.activation)
        discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        autoencoder_input = Input(shape=(self.n1,))
        reconstructed_input = Input(shape=(self.n1,))
        encoded_repr = encoder(autoencoder_input)
        reconstructed = decoder(encoded_repr)

        # For the adversarial_autoencoder model we will only train the generator
        discriminator.trainable = False

        # The discriminator determines validity of the encoding
        validity = discriminator(encoded_repr)

        # The adversarial_autoencoder model  (stacked generator and discriminator)
        adversarial_autoencoder = Model(autoencoder_input, [reconstructed, validity])

        ##hp_learning_rate = hp.Float('learning_rate', min_value=1e-4, max_value=0.01, sampling='LOG')

        # train_model =AAE(n1,n2,n3,n4,batch_size,activation,hp_learning_rate,50)
        # train_model.train()
        adversarial_autoencoder.compile(optimizer=optimizer, loss=['mse', 'binary_crossentropy'],
                                        loss_weights=[0.999, 0.001])
        # autoencoder.compile(optimizer=RMSprop(learning_rate=hp_learning_rate), loss="binary_crossentropy", metrics=['accuracy'])
        # autoencoder.compile(optimizer=Adagrad(learning_rate=hp_learning_rate), loss="binary_crossentropy", metrics=['accuracy'])
        # autoencoder.compile(optimizer=Adam(learning_rate=hp_learning_rate), loss="binary_crossentropy", metrics=['accuracy'])
        return adversarial_autoencoder

    def fit(self, hp, adversarial_autoencoder, *args, **kwargs):
        batch_size = hp.Int('batch_size', min_value=16, max_value=128, step=8)
        encoder = layers.build_encoder(self.n1, self.n2, self.n3, self.n4, self.activation)
        decoder = layers.build_decoder(self.n1, self.n2, self.n3, self.n4, self.activation)
        discriminator = layers.build_discriminator(self.n1, self.n2, self.n3, self.n4, self.activation)
        #optimizer = RMSprop(learning_rate=0.00002)
        if self.learningrate is None:
            optimizer = opt.__dict__[self.optimizer]()
        else:
            optimizer = opt.__dict__[self.optimizer](lr=self.learningrate)
            
        discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        # For the adversarial_autoencoder model we will only train the generator
        discriminator.trainable = False

        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        
        for epoch in np.arange(1, self.hyperepoch + 1):
            for i in range(int(len(self.X_train) / batch_size)):
                # ---------------------
                #  Train Discriminator
                # ---------------------

                # Select a random batch of images
                batch = self.X_train[i * batch_size:i * batch_size + batch_size]

                latent_fake = encoder.predict(batch)
                latent_real = np.random.normal(size=(batch_size, self.n4))

                # Train the discriminator
                d_loss_real = discriminator.train_on_batch(latent_real, valid)
                d_loss_fake = discriminator.train_on_batch(latent_fake, fake)
                d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

                # ---------------------
                #  Train Generator
                # ---------------------

                # Train the generator
                g_loss = adversarial_autoencoder.train_on_batch(batch, [batch, valid])

        return 100 * d_loss[1]

    #    return adversarial_autoencoder.fit(
    #        *args,
    #        batch_size=hp.Int('batch_size', min_value = 16, max_value = 128, step = 8),
    #        **kwargs,
    # )

