import sys, argparse

def vce(k,p):
    """Vigenere cipher: Cipher_i = (Plain_i + Key_i) mod 26"""
    
    from itertools import cycle
    ki=cycle(k)
    c=""
    for pi in p:
        c = c + chr(65 + ( ( ord(pi) - 65 ) + ( ord( next(ki) ) - 65 ) ) % 26)
    return c

def vcd(k,c):
    """Vigenere Decipher: Plain_i = (Cipher_i - Key_i) mod 26"""

    from itertools import cycle
    ki=cycle(k)
    p=""
    for ci in c:
        p = p + chr(65 + (( ord(ci) - 65 ) - ( ord(next(ki)) - 65 )) % 26)
    return p

def test():
    test_plain="MAKEITHAPPEN"
    test_key="MATH"
    test_cipher="YADLUTAHBPXU"
    print "Plain:  ", test_plain
    print "vce:    ", vce(test_key, test_plain)
    print "Cipher: ", test_cipher
    print "vcd:    ", vcd(test_key,test_cipher)

def main(argv):
    description = "Vigenere cipher"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('oper', choices=['e', 'd'], help="encrypt or decrypt")
    parser.add_argument('-k', metavar='key', help='cipher key')
    parser.add_argument('-i', metavar='in-file', type=argparse.FileType('rt'), help='the file to process')
    args = parser.parse_args()

    for i, line in enumerate(args.i):
        print vcd(args.k,line[:-1]) if args.oper == 'd' else vce(args.k,line[:-1])

if __name__ == "__main__":
   main(sys.argv[1:])
