import jieba
import OpenHowNet
from gensim.models import Word2Vec
import re
from zhon.hanzi import punctuation

window_size = 1
hownet_dict = OpenHowNet.HowNetDict()


# read the dataset and here must encoding as gb18030
def readFile(filename):
    with open(filename, 'r', encoding='gb18030') as f:
        text = ""
        line = f.readline()
        while line:
            text += preprocess(line)
            line = f.readline()
    return text


# clean the dataset
def preprocess(line):
    # remove number
    line = re.sub(r'[0-9]+', '', line)
    # remove punctuation
    line = re.sub(r'[^\w\s]', '', line)
    # remove tabs
    line = re.sub(r'[\t|\n]', ' ', line)
    line = line.strip()
    line = re.sub("[{}]+".format(punctuation), " ", line)
    return line


def train_w2v(corpus_filename):
    l = []
    count = 0
    with open(corpus_filename, 'r', encoding='gb18030') as f:
        line = f.readline()
        li = []
        while count < 10000:
            line = preprocess(line)
            result = jieba.cut(line)
            for i in result:
                li.append(i)
            l.append(li)
            count += 1
            line = f.readline()

    model = Word2Vec(l, min_count=1)
    result = model.wv['苹果']
    model.save('./w2v.model')
    print(result)


if __name__ == '__main__':
    # test sentence
    test_sentence = "这个苹果真好吃"
    word = "苹果"
    # train a word2vec model
    train_w2v("../../dataset/harrypotterChinese.txt")
    # compare similarity of target and meaning answer