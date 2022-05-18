from tokenizers import BertWordPieceTokenizer
from transformers import BertTokenizerFast, DistilBertTokenizerFast
import config

if config.NEW_VOCAB:
    tokenizer = BertWordPieceTokenizer(handle_chinese_chars=False, lowercase=False)
    # Customize training, Limit Vocab_Size and special tokens to thoese in BERT paper.
    tokenizer.train(files=config.TRAIN_DATA_PATH,
                    vocab_size=30000,
                    min_frequency=2,
                    show_progress=True,
                    special_tokens=[
                        "[PAD]",
                        "[CLS]",
                        "[UNK]",
                        "[MASK]",
                        "[SEP]"
                    ])

    tokenizer.save_model(config.TOKENIZER_LOCAL_DIR)
    tokenizer = BertTokenizerFast.from_pretrained(config.TOKENIZER_LOCAL_DIR, max_len=config.MAX_LEN,
                                                  handle_chinese_chars=False, lowercase=False, local_files_only=True)
else:
    if 'distil' in config.MODEL_NAME:
        tokenizer = DistilBertTokenizerFast.from_pretrained(config.MODEL_NAME, max_len=config.MAX_LEN,
                                                      handle_chinese_chars=False,
                                                      lowercase=False, local_files_only=True)
    else:
        tokenizer = BertTokenizerFast.from_pretrained(config.MODEL_NAME, max_len=config.MAX_LEN, handle_chinese_chars=False,
                                                  lowercase=False, local_files_only=True)