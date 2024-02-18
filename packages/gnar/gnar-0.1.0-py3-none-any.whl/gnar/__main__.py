from . import *

def _main():
    this = "." | ls() | cat() | sed(r"dependencies", r"that")
    print(this)


if __name__ == "__main__":
    _main()
