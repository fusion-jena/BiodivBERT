from os import makedirs
from os.path import join, exists

Abstracts = False
# if NEW_VOCAB the tokenizer would be customized to our vocab only
NEW_VOCAB = False

# Model
# MODEL_NAME = 'bert-base-cased'
MODEL_NAME = 'distilbert-base-cased'

#Paths
root = join('/', 'xyz', 'xyz') # TODO: Point to your data dir

if Abstracts:
    data_root = join(root, 'BiodivBERT', 'abstracts')
    LOCAL_DIR = join(root, 'biodiv{}-abs'.format(MODEL_NAME))  # were the model is saved
else:
    data_root = join(root, 'BiodivBERT', 'fulltxt')
    LOCAL_DIR = join(root, 'biodiv{}-full'.format(MODEL_NAME))  # were the model is saved

TRAIN_DATA_PATH = join(data_root, 'train.txt') #file
TEST_DATA_PATH = join(data_root, 'test.txt') #file

# local dir for pre-trained BiodivBERT
if not exists(LOCAL_DIR):
    makedirs(LOCAL_DIR)

# create new dir for tokenizer if NEW_VOCAB
if NEW_VOCAB:
    TOKENIZER_LOCAL_DIR = join(LOCAL_DIR, 'tokenizer') # were the tokenizer is saved
    # where the tokenizer should be saved
    if not exists(TOKENIZER_LOCAL_DIR):
        makedirs(TOKENIZER_LOCAL_DIR)

# if True it starts a training from sratch otherwise, resume from the provided checkpoint
train_from_sratch = True
CHECKPOINT_NAME = None

# Model
MODEL_NAME = 'bert-base-cased'

# Tokenizer & LineByLineDataset
MAX_LEN = 512 # Default of BERT && Recommended by Luise

# Data Collator
MLM_PROP = 0.15

# Trainer
num_train_epochs = 3 # the minimum sufficient epochs found on many articles && default of trainer here
per_device_train_batch_size = 16 # the maximumn that could be held by V100 on Ara with 512 MAX_LEN was 8 in the old run
per_device_eval_batch_size = 16 # usually as above
gradient_accumulation_steps = 4 # this will grant a minim batch size 16 * 4 * nGPUs.





