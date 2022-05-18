from os import listdir, makedirs
from os.path import join, realpath, exists

root_dir = join(realpath('.'), 'Data')
CLEANED_DATA_PATH = join(root_dir, 'clean')


def run():
    Train_Test_Split = 0.2
    paths = listdir(CLEANED_DATA_PATH)

    print("Load the entire dataset sentences")

    sentences = []
    for i, path in enumerate(paths):
        with open(join(CLEANED_DATA_PATH, path), 'r', encoding='utf8') as file:
            lines = file.read().splitlines()
            # the entire dataset is in memory, we should consider patching?
            # an idea:  we could load the entire dataset file by file, calculate how many the overall sentences then
            # loop again based on  the specific train/test portion
            sentences.extend(lines)

    print("#Sentences: {}".format(len(sentences)))

    FINAL_DATA_PATH = join(root_dir, 'FullTxt')
    if not exists(FINAL_DATA_PATH):
        makedirs(FINAL_DATA_PATH)
    TRAIN_DATA_PATH = join(FINAL_DATA_PATH, 'train.txt')
    TEST_DATA_PATH = join(FINAL_DATA_PATH, 'test.txt')

    # split to 80% in train.txt and 20% to test.txt
    with open(join(TRAIN_DATA_PATH), 'w', encoding='utf8') as file:
        file.write('\n'.join([s for s in  sentences[0:int((1-Train_Test_Split)*len(sentences))] if len(s) > 1]))
    print("Stored training data at: ", TRAIN_DATA_PATH)

    with open(join(TEST_DATA_PATH), 'w', encoding='utf8') as file:
        file.write('\n'.join([s for s in sentences[int((1-Train_Test_Split)*len(sentences))+1::] if len(s) > 1]))
    print("Stored testing data at: ", TEST_DATA_PATH)


if __name__ == '__main__':
    run()
