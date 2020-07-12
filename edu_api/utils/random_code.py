
import random

def get_random_code():

    code = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        code += ch

    return code


if __name__ =="__main__":

    # get_random_code()
    print(get_random_code())