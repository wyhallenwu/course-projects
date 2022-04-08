import re
import jieba


def read_file(filename):
    content = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            content.append(line)
            line = f.readline()
    return content


if __name__ == '__main__':
    content = read_file("./mmseg/dataset/raw.txt")
    result = []
    for sentence in content:
        segList = jieba.cut(sentence, cut_all=False)
        result.append('_'.join(segList))

    # export result to file
    with open("./result/jieba_cut_result.txt", 'w') as f:
        for r in result:
            f.write(str(r) + '\n')

    print("export result to file end\n")