import sys
from TreeBuilder import buildParseTree

def main(argv):
    tree = buildParseTree('test.qasm')
    pass

if __name__ == '__main__':
    main(sys.argv)