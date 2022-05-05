from ltp import LTP
import json


def readFile(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = []
        line = f.readline()
        while line:
            text.append(str(line))
            line = f.readline()
    return text


def write2json(result, filename):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(result, f, indent=4)
    print("write over...")


if __name__ == '__main__':
    ltp = LTP()
    text = readFile("../lab2/mmseg/dataset/raw.txt")
    result = []
    for i in text:
        _, hidden = ltp.seg([i])
        srl = ltp.srl(hidden=hidden)
        result.append(srl)

    write2json(result, "./srl_result.txt")
