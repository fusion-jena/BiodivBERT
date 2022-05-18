from datasets import load_dataset
from get_tokenizer import *

from util_log import log
import config

block_size = config.MAX_LEN

def group_texts(examples):
    # Concatenate all texts.
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
        # customize this part to your needs.
    total_length = (total_length // block_size) * block_size
    # Split by chunks of max_len.
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result

def tokenize_function(examples):
    return tokenizer(examples["text"])

def get_torch_datasets():
    datasets = load_dataset("text", data_files={"train": config.TRAIN_DATA_PATH, "validation": config.TEST_DATA_PATH})
    log.info('10th Train Example: {}'.format(datasets["train"][10]))

    log.info("Tokenizing Datasets...")
    tokenized_datasets = datasets.map(tokenize_function,
                                      batched=True,
                                      batch_size=10000,
                                      num_proc=8,
                                      remove_columns=["text"])

    log.info("Padding/Truncating Datasets...")
    lm_datasets = tokenized_datasets.map(
        group_texts,
        batched=True,
        batch_size=10000,
        num_proc=8,
    )

    return lm_datasets
