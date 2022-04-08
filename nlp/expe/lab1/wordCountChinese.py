import argparse
import jieba
import re
from zhon.hanzi import punctuation
import json
import numpy as np


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


# do segmentation for dataset
def segmentation(text):
    segList = jieba.lcut(text)
    return segList


# countWords sum the frequency of each word
def countWords(segList):
    counts = {}
    for word in segList:
        counts[word] = counts.get(word, 0) + 1

    # sort
    countList = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return countList


# pipeline is the whole process from reading dataset to get frequency list
def pipeline(filename):
    text = readFile(filename)
    segList = segmentation(text)
    counts = countWords(segList)
    return counts


# get topK words' frequency list
def GetTopK(k, counts):
    return counts[:k]


# compute entropy for topK words
def getEntropy(k, counts):
    counts = GetTopK(k, counts)
    count_all = sum(freq[1] for freq in counts)
    probability = list([freq[1] / count_all for freq in counts])
    entropy = (-1) * sum(p * np.log2(p) for p in probability)
    print("entropy is: ", entropy)


# write the topK words frequency list to a json file
def write2json(freqList, filename):
    with open(filename, 'w', encoding="gb18030") as f:
        json.dump(freqList, f, ensure_ascii=False, indent=4)
    print("write over...")


def countChar(text):
    counts = {}
    for c in text:
        counts[c] = counts.get(c, 0) + 1

    countList = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    write2json(countList, "./result/all_frequency_single_char.json")
    getEntropy(len(countList), countList)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',
                        '--filename',
                        required=True,
                        help='please input file path',
                        action='store')
    parser.add_argument("--list",
                        "-l",
                        nargs="+",
                        type=int,
                        help="please input topK number")
    args = parser.parse_args()
    filename = args.filename
    li = args.list

    counts = pipeline(filename)
    for i in li:
        print(getEntropy(i, counts))
    # write2json(counts, "./result/all_frequency_chinese.json")
    countChar(readFile(filename))