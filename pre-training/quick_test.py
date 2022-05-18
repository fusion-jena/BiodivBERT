from transformers import pipeline
from transformers import BertTokenizerFast
from config import *
import pprint

# pretty print for debugging
pp = pprint.PrettyPrinter(indent=4)


def run():
    # init the same type of tokenizer used in training
    if NEW_VOCAB:
        tokenizer = BertTokenizerFast.from_pretrained(TOKENIZER_LOCAL_DIR, max_len=MAX_LEN, local_files_only=True)
    else:
        tokenizer = BertTokenizerFast.from_pretrained(MODEL_NAME, max_len=MAX_LEN, local_files_only=True)

    # use ready made pipeline named fill-mask to operate out of the box
    fill_mask = pipeline(
        "fill-mask",
        model=LOCAL_DIR,
        tokenizer=tokenizer
    )

    # a static testing case
    test_case = "Diversification and [MASK] in brood pollination mutualisms."

    print('Quick LM Test: ')
    print('.............  test case: {}\n'.format(test_case))

    reslst = fill_mask(test_case)

    [print(resi) for resi in reslst]

    # Excepted  Output
    # [{'score': 0.22341474890708923,
    #   'sequence': 'Diversification and variation in brood pollination mutualisms.',
    #   'token': 8516,
    #   'token_str': 'variation'},
    #  {'score': 0.10778778046369553,
    #   'sequence': 'Diversification and diversity in brood pollination mutualisms.',
    #   'token': 9531,
    #   'token_str': 'diversity'},
    #  {'score': 0.042027778923511505,
    #   'sequence': 'Diversification and changes in brood pollination mutualisms.',
    #   'token': 2607,
    #   'token_str': 'changes'},
    #  {'score': 0.03849424794316292,
    #   'sequence': 'Diversification and variations in brood pollination mutualisms.',
    #   'token': 9138,
    #   'token_str': 'variations'},
    #  {'score': 0.033782992511987686,
    #   'sequence': 'Diversification and change in brood pollination mutualisms.',
    #   'token': 1849,
    #   'token_str': 'change'}]

if __name__ == '__main__':
    run()