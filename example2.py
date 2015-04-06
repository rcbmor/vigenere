#!/usr/bin/env python

"""Functions for encrypting and decrypting text using
   the Vigenere square cipher. See:
   http://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher

   IC stands for Index of Coincidence:
   http://en.wikipedia.org/wiki/Index_of_coincidence
"""

from __future__ import division
from collections import Counter
from math import fabs
from string import ascii_lowercase
from scipy.stats import pearsonr
from numpy import matrix
from os import system

#Define some constants:
LETTER_CNT = 26
ENGLISH_IC = 1.73

#Cornell English letter frequecy
#http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
ENGLISH_LETTERS = 'etaoinsrhdlucmfywgpbvkxqjz'
ENGLISH_FREQ = [0.1202, 0.0910, 0.0812, 0.0768, 0.0731, 0.0695, 0.0628,
                0.0602, 0.0592, 0.0432, 0.0398, 0.0288, 0.0271, 0.0261,
                0.0230, 0.0211, 0.0209, 0.0203, 0.0182, 0.0149, 0.0111,
                0.0069, 0.0017, 0.0011, 0.0010, 0.0007]
ENGLISH_DICT = dict(zip(list(ENGLISH_LETTERS), ENGLISH_FREQ))
MAX_LEN = 10    #Maximum keyword length


def scrub_string(str):
    """Remove non-alphabetic characters and convert string to lower case. """
    return ''.join(ch for ch in str if ch.isalpha()).lower()


def string_to_numbers(str):
    """Convert str to a list of numbers giving the position of the letter
    in the alphabet (position of a = 0). str should contain only
    lowercase letters.
    """
    return [ord(ch) - ord('a') for ch in str]


def numbers_to_string(nums):
    """Convert a list of numbers to a string of letters
    (index of a = 0); the inverse function of string_to_numbers.
    """
    return ''.join(chr(n + ord('a')) for n in nums)


def shift_string_by_number(str, shift):
    """Shift the letters in str by the amount shift (either positive
    or negative) modulo 26.
    """
    return numbers_to_string((num + shift) % LETTER_CNT
                             for num in string_to_numbers(str))


def shift_string_by_letter(str, ch, direction):
    """Shift the letters in str by the value of ch, modulo 26.
    Right shift if direction = 1, left shift if direction = -1.
    """
    assert direction in {1, -1}
    return shift_string_by_number(str, (ord(ch) - ord('a') + 1) * direction)


def chunk_string(str):
    """Add a blank between each block of five characters in str."""
    return ' '.join(str[i:i+5] for i in xrange(0, len(str), 5))


def crypt(text, passphrase, which):
    """Encrypt or decrypt the text, depending on whether which = 1
    or which = -1.
    """
    text = scrub_string(text)
    passphrase = scrub_string(passphrase)
    letters = (shift_string_by_letter(ch, passphrase[i % len(passphrase)], which)
                   for i, ch in enumerate(text))
    return ''.join(letters)


def IC(text, ncol):
    """Divide the text into ncol columns and return the average index
    of coincidence across the columns.
    """
    text = scrub_string(text)
    A = str_to_matrix(scrub_string(text), ncol)
    cum = 0
    for col in A:
        N = len(col)
        cum += (sum(n*(n - 1) for n in Counter(col).values())
                / (N*(N - 1)/LETTER_CNT))
    return cum/ncol


def keyword_length(text):
    """Determine keyword length by finding the length that makes
    IC closest to the English plaintext value of 1.73.
    """
    text = scrub_string(text)
    a = [fabs(IC(text, ncol) - ENGLISH_IC) for ncol in xrange(1, MAX_LEN)]
    return a.index(min(a)) + 1


def correlation(letter_list):
    """Return the correlation of the frequencies of the letters
    in the list with the English letter frequency.
    """
    counts = Counter(letter_list)
    text_freq = [counts[ch]/len(letter_list) for ch in ascii_lowercase]
    english_freq = [ENGLISH_DICT[ch] for ch in ascii_lowercase]
    return pearsonr(text_freq, english_freq)[0]


def find_keyword_letter(letter_list):
    """Return a letter of the keyword, given every nth character
    of the ciphertext, where n = keyword length.
    """
    str = ''.join(letter_list)
    cors = [correlation(shift_string_by_number(str, -num))
            for num in xrange(1, LETTER_CNT + 1)]
    return ascii_lowercase[cors.index(max(cors))]


def find_keyword(ciphertext, keyword_length):
    """Return the keyword, given its length and the ciphertext."""
    A = str_to_matrix(scrub_string(ciphertext), keyword_length)
    return ''.join(
        [find_keyword_letter(A[j]) for j in xrange(keyword_length)])


def str_to_matrix(str, ncol):
    """Divide str into ncol lists as in the example below:

    >>> str_to_matrix('abcdefghijk', 4)
    [['a', 'e', 'i'], ['b', 'f', 'j'], ['c', 'g', 'k'], ['d', 'h']]
    """
    A = [list(str[i:i + ncol]) for i in xrange(0, len(str), ncol)]
    stub = A.pop()
    B = matrix(A).T.tolist()
    for i, ch in enumerate(stub):
        B[i] += ch
    return B


def test_functions():
    """Unit tests for functions in this module."""
    assert(shift_string_by_number('unladenswallow', 15) == 'jcapstchlpaadl')
    assert(shift_string_by_letter('unladenswallow', 'M', -1) == 'ngetwxglpteehp')
    assert(chunk_string('terpsichorean') == 'terps ichor ean')
    assert(crypt('Hello world!', "mypassword", 1) == 'udbmhplgdh')
    assert(crypt('udbmhplgdh', "mypassword", -1) == 'helloworld')
    assert(round(correlation('ganzunglabulich'), 6) == 0.118034)

    assert(scrub_string("I'm not Doctor bloody Bernofsky!!") ==
    'imnotdoctorbloodybernofsky')

    assert(string_to_numbers('lemoncurry') ==
    [11, 4, 12, 14, 13, 2, 20, 17, 17, 24])

    assert(numbers_to_string([11, 4, 12, 14, 13, 2, 20, 17, 17, 24]) ==
    'lemoncurry')

    assert(round(IC('''QPWKA LVRXC QZIKG RBPFA EOMFL JMSDZ VDHXC XJYEB IMTRQ
    WNMEA IZRVK CVKVL XNEIC FZPZC ZZHKM LVZVZ IZRRQ WDKEC
    HOSNY XXLSP MYKVQ XJTDC IOMEE XDQVS RXLRL KZHOV''', 5)
                 , 2) ==  1.82)

    assert(keyword_length('''QPWKA LVRXC QZIKG RBPFA EOMFL JMSDZ VDHXC XJYEB
    IMTRQ WNMEA IZRVK CVKVL XNEIC FZPZC ZZHKM LVZVZ IZRRQ WDKEC
    HOSNY XXLSP MYKVQ XJTDC IOMEE XDQVS RXLRL KZHOV''') == 5)

    assert(str_to_matrix('abcdefghijk', 4) ==
    [['a', 'e', 'i'], ['b', 'f', 'j'], ['c', 'g', 'k'], ['d', 'h']])


if __name__ == '__main__':
    print 'Calculating...'
    with open ("plaintext.txt", "r") as infile:
        plaintext = infile.read().replace('\n', ' ')
    passphrase = 'Moby Dick'
    ciphertext =  crypt(plaintext, passphrase, 1)
    kw_len = keyword_length(ciphertext)
    kw = find_keyword(ciphertext, kw_len)
    print 'Keyword length is {0}.'.format(kw_len)
    print 'The keyword is {0}.'.format(kw)
    system("""bash -c 'read -s -n 1 -p "Press any key print the decrypted text..."'""")
    print crypt(ciphertext, kw, -1)