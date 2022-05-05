from telnetlib import WONT
import jieba
import OpenHowNet
import numpy as np
from gensim.models import Word2Vec, KeyedVectors
import re
from zhon.hanzi import punctuation

# window_size = 1
# hownet_dict = OpenHowNet.HowNetDict()


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


def sen_vector_compute(segList):
    result = np.zeros(100)
    l = 0
    for i in segList:
        result += wv_from_text.wv[i]
        l += 1.0
    return result / l


def computer_similarity(v1, v2):
    numerator = 0
    v1_sum, v2_sum = 0, 0
    # each vector has 100 dimentions
    for i in range(100):
        numerator += v1[i] * v2[i]
        v1_sum += v1[i]**2
        v2_sum += v2[i]**2
    denominator = np.sqrt(v1_sum) * np.sqrt(v2_sum)
    return numerator / denominator


if __name__ == '__main__':
    # test sentence
    target = "人体需要水分"
    compare1 = "植物从土壤中吸收水分"
    compare2 = "他的话里有很大水分"
    test_sentence = [target, compare1, compare2]
    flag = False
    # train a word2vec model
    if flag:
        train_w2v("../../dataset/harrypotterChinese.txt")
    else:
        # compare similarity of target and meaning answer
        # model = Word2Vec.load("./w2v.model")
        # v = []
        # for i in test_sentence:
        #     segList = jieba.cut(i)
        #     result = sen_vector_compute(segList)
        #     v.append(result)
        # print(v)

        # https://ai.tencent.com/ailab/nlp/zh/download.html
        # tencent pretrained wv, I use v0.2.0 100dim small
        wv_from_text = KeyedVectors.load_word2vec_format(
            "../../tencent-ailab-embedding-zh-d100-v0.2.0-s/tencent-ailab-embedding-zh-d100-v0.2.0-s.txt",
            binary=False)
        v = []
        for i in test_sentence:
            segList = jieba.cut(i)
            result = sen_vector_compute(segList)
            print(result.shape)
            v.append(result)
        s1 = computer_similarity(v[0], v[1])
        s2 = computer_similarity(v[0], v[2])
        print(s1, s2)
        # s1 = 0.8526, s2 = 0.7810
