import argparse
from . import gen_pair

if __name__ == '__main__':
    for _ in range(10):
        print(gen_pair())
