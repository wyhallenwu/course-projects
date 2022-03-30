from ltp import LTP


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
    text = readFile('../lab2/mmseg/dataset/raw.txt')
    ltp = LTP()
    result = []
    for sentence in text:
        seg, hidden = ltp.seg([sentence])
        dep = ltp.dep(hidden)
        result.append(dep)
    for r in result:
        print(r)
        print('\n')