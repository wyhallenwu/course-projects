import argparse
import jieba
import re
from zhon.hanzi import punctuation
import json


def readFile(filename):
    with open(filename, 'r', encoding='gb18030') as f:
        text = ""
        line = f.readline()
        while line:
            text += preprocess(line)
            line = f.readline()
    return text


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


def segmentation(text):
    segList = jieba.lcut(text)
    return segList


def countWords(segList):
    counts = {}
    for word in segList:
        counts[word] = counts.get(word, 0) + 1

    # sort
    countList = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return countList


def pipeline(filename):
    text = readFile(filename)
    segList = segmentation(text)
    counts = countWords(segList)
    return counts


def GetTopK(k):
    return counts[:k]


def write2json(freqList, filename):
    with open(filename, 'w', encoding="gb18030") as f:
        json.dump(freqList, f, ensure_ascii=False, indent=4)
    print("write over...")


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
    # for i in li:
    #     print(GetTopK(i))
    write2json(counts, "./result/all_frequency_chinese.json")