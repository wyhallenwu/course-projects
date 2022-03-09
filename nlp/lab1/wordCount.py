from nltk.tokenize import word_tokenize
import nltk
import re
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import argparse


def GetAllFreq():
    with open("../dataset/harrypotterall.txt", "r", encoding="gbk") as f:
        line = f.readline()
        text = ""
        while line:
            text += preprocess(line)
            line = f.readline()
    wordList = countWords(text)
    freq = nltk.FreqDist(wordList)
    # sort by frequency
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    write2json(freq, "./result/all_frequency.json")


# count words' frequency
def countWords(text):
    wordList = word_tokenize(text)
    return wordList


# preprocess sentences
def preprocess(line):
    # remove number
    line = re.sub(r'[0-9]+', '', line)
    # remove punctuation
    line = re.sub(r'[^\w\s]', '', line)
    # remove tabs
    line = re.sub(r'[\t|\n]', ' ', line)
    return str(line).lower()


def write2json(freqList, filename):
    with open(filename, 'w') as f:
        json.dump(freqList, f, indent=4)
    print("write over...")


def readFromAll():
    with open("./result/all_frequency.json", "r") as f:
        freqList = json.load(f)
    return freqList


# set x axis space
def tickSpace(k):
    if k > 2000:
        return 600
    elif k > 1000:
        return 400
    elif k > 100:
        return 120
    elif k > 20:
        return 20
    else:
        return 5


def GetTopK(k):
    freqList = readFromAll()
    wordList = []
    freq = []
    for i in range(k):
        wordList.append(freqList[i][0])
        freq.append(freqList[i][1])

    _, ax = plt.subplots(1, 1)
    ax.plot(wordList, freq)
    plt.xlabel('word')
    plt.ylabel('frequency')
    plt.title("Top " + str(k) + " frequency")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tickSpace(k)))
    plt.savefig("./result/top" + str(k) + ".png", dpi=500)
    print("save fig" + str(k))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--list",
                        "-l",
                        nargs="+",
                        type=int,
                        help="please input topK number")

    args = parser.parse_args()
    li = args.list
    print("get topK: ", li)
    for i in li:
        GetTopK(i)
    GetAllFreq()