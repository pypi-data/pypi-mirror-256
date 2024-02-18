# Copyright 2024 Kyung Dae Ko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Adversarial Autoencoder')

    parser.add_argument('input', type=str, help='Input is raw count data in TSV/CSV '
                                                'or H5AD (anndata) format. '
                                                'Row/col names are mandatory. Note that TSV/CSV files must be in '
                                                'gene x cell layout where rows are genes and cols are cells (scRNA-seq '
                                                'convention).'
                                                'Use the -t/--transpose option if your count matrix in cell x gene layout. '
                                                'H5AD files must be in cell x gene format (stats and scanpy convention).')
    parser.add_argument('outputdir', type=str, help='The path of the output directory')

    parser.add_argument('-g', '--genenum', type=int, default=4000,
                        help="number of gene with high variance to detect (default: 4000) ")

    parser.add_argument('-b', '--batchsize', type=int, default=32,
                        help="Batch size (default:32)")
    
    parser.add_argument('-ld', '--latent_dim', type=int, default=512,
                        help="Batch size (default:32)")

    parser.add_argument('--activation', type=str, default='relu',
                        help="Activation function of hidden units (default: relu)")
    parser.add_argument('--optimizer', type=str, default='RMSprop',
                        help="Optimization method (default: RMSprop)")
    parser.add_argument('-e', '--epochs', type=int, default=20,
                        help="Max number of epochs to continue training in case of no "
                             "improvement on validation loss (default: 300)")
    parser.add_argument('-r', '--learningrate', type=float, default=None,
                        help="Learning rate (default: 0.001)")
    parser.add_argument('--dynamic', dest='dynamic',
                        action='store_true', help="Optimizer batch size (default: False)")
    parser.add_argument('--train', dest='train',
                        action='store_true', help="Optimizer batch size (default: False)")
    parser.add_argument('--hypern', dest='hypern', type=int, default=1000,
                        help="Number of samples drawn from hyperparameter distributions during optimization. "
                             "(default: 1000)")
    parser.add_argument('--hyperepoch', dest='hyperepoch', type=int, default=100,
                        help="Number of epochs used in each hyperpar optimization iteration. "
                             "(default: 100)")

    parser.set_defaults(dynamic=False)

    return parser.parse_args()


def main():
    
    args = parse_args()

    try:
        import tensorflow as tf
    except ImportError:
        raise ImportError('AAE requires TensorFlow v2+. Please follow instructions'
                          ' at https://www.tensorflow.org/install/ to install'
                          ' it.')

    # import tf and the rest after parse_args() to make argparse help faster
    # from . import train
    from utils import io,train
    import random
    import time
    import datetime
    import pandas as pd

    random.seed(1234)
    
    print(args)

    print("Loading data...")
    adata=io.read_dataset(args.input,highly_genes=args.genenum)
    
    n1=5000
    n2=1024
    n3=512
    n4=args.latent_dim
    batch_size = args.batchsize
    n_epochs = args.epochs
    X_train = pd.DataFrame(adata.X)
    X_train =X_train.to_numpy()
    activation=args.activation
    optimizer=args.optimizer
    learningrate=args.learningrate
    hyperepoch=args.hyperepoch
    start_time = time.time()

    if args.dynamic :
        from utils import dynamic
        import keras_tuner as kt
        import tensorflow as tf
       # dynamic.AEHyperModel(X_train, n1,n2,n3,n4,learningrate,activation,optimizer)
          
        tuner = kt.Hyperband(dynamic.AEHyperModel(X_train,n1,n2,n3,n4,hyperepoch,learningrate,activation,optimizer),
                    objective = 'val_accuracy',
                    max_epochs = 10,
                    executions_per_trial = 1,
                    overwrite = True,
                     directory = './cache',
                     max_consecutive_failed_trials=5,
                    factor = 3)
        
        stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', mode='max', baseline=100)
        tuner.search(X_train, X_train, epochs = 10, validation_split = 0.1, callbacks=[stop_early])
        
        best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

        print(f"""batch_size : {best_hps.get('batch_size')}""")
        batch_size = best_hps.get('batch_size')
        adversarial_autoencoder=train.train(X_train,n1,n2,n3,n4,batch_size,n_epochs,learningrate,activation,optimizer)
        adversarial_autoencoder.summary()
        rlt_dir=args.outputdir
        current_time = datetime.datetime.now()
    
        adversarial_autoencoder.save(rlt_dir+'{}'.format("DB_AAE")+'_'+str(current_time.year)+'_'+str(current_time.month)+'_'+
                                 str(current_time.day)+'_'+str(current_time.hour)+'_'+str(current_time.minute)+'.h5')
    
    if args.train :
        
        adversarial_autoencoder=train.train(X_train,n1,n2,n3,n4,batch_size,n_epochs,learningrate,activation,optimizer)
        adversarial_autoencoder.summary()
        rlt_dir=args.outputdir
        current_time = datetime.datetime.now()
    
        adversarial_autoencoder.save(rlt_dir+'{}'.format("DB_AAE")+'_'+str(current_time.year)+'_'+str(current_time.month)+'_'+
                                 str(current_time.day)+'_'+str(current_time.hour)+'_'+str(current_time.minute)+'.h5')
    
    

if __name__ == "__main__":
    main()
