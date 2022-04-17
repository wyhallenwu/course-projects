from dis import pretty_flags
from ltp import LTP
import json


# read the dataset and here must encoding as gb18030
def readFile(filename):
    text = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            text.append(line)
            line = f.readline()
    return text


def write2json(result, filename):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(result, f, indent=4)
    print("write over...")


if __name__ == '__main__':
    text = readFile('../lab2/mmseg/dataset/raw.txt')
    ltp = LTP(pretty_flags=True)
    result = []
    for sentence in text:
        seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        result.append(dep)
    write2json(result, "./result/hitltp_result.txt")