import re
import jieba


def read_file(filename):
    content = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            content.append(str(line))
    return content


if __name__ == '__main__':
    content = read_file("./mmseg/dataset/raw.txt")
    result = []
    for sentence in content:
        segList = jieba.cut(sentence, cut_all=True)
        result.append(segList)
    print(result)