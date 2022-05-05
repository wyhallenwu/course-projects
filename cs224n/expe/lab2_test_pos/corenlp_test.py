from pyhanlp import *


# read the dataset and here must encoding as gb18030
def readFile(filename):
    text = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            text.append(line)
            line = f.readline()
    return text


if __name__ == '__main__':
    text = readFile("../lab2/mmseg/dataset/raw.txt")
    result = []
    for sentence in text:
        s_dep = HanLP.parseDependency(sentence)
        result.append(s_dep)
    with open("./result/hanlp_result.txt", 'w') as f:
        for i in result:
            f.write(str(i))
    print("write over...")