# coding=utf-8
import sys

if __name__ == '__main__':
    train_path = open('train.data', 'w')
    test_path = open('test.data', 'w')
    idx = 0
    for line in open(sys.argv[1]):
        if idx % 4 == 0:
            test_path.write(line)
        else:
            train_path.write(line)
        idx += 1
