import sys, argparse
import operator

def calculate_factors(num):
    _factors = []
    for i in range(4, num):
        if num % i == 0:
            _factors.append(i)
    return _factors

def minus1(v):
    return v-1

def friedman(cipher):

    letters = map(chr, range(65, 91))
    # Count letters.
    freq = dict((key, cipher.count(key)) for key in letters)
    print "freq: ", freq
    v1 = freq.values()
    n = sum(v1)

    v2 = map(minus1,v1)
    v3 = [a*b for a,b in zip(v1,v2)]
    nn = sum(v3)

    # index of coincidence => Equation #5 in article
    ic = nn / (float)(n * (n-1))
    
    # key length => measure of roughness - deviation from a flat frequency
    l = (0.027 * n) / (((n - 1) * ic) - (0.038 * n) + 0.065)

    return (ic,l)


def kasinski(cipher, sz=3):
    #
    # step 1 - find trigram's repetition distances
    #
    trigrams = {}

    for i in xrange(0,len(cipher)):
        trigram = cipher[i:i+sz]
        if not trigrams.has_key(trigram):
            distances = []
            pos = cipher.find(trigram, i+sz)
            while pos > -1:
                diff = pos - i
                distances.append(diff)
                pos = cipher.find(trigram, pos+sz)
            if len(distances):
                trigrams[trigram] = distances

    def lencmp(x,y):
        return len(x) - len(y)

    sorted_x = sorted(trigrams.items(), key=operator.itemgetter(1), cmp=lencmp, reverse=True)
    maxl = len(sorted_x)
    maxl = maxl if maxl < 5 else 5
    #print "==> Trigrams"
    #for i in range(maxl):
    #    print sorted_x[i]

    #
    # step 2 - find common factors for all distances
    #
    alldistances = {}
    for (tr,ds) in trigrams.items():
        for d in ds:
            if alldistances.has_key(d):
                alldistances[d] = alldistances[d] + 1
            else:
                alldistances[d] = 0

    sorted_x = sorted(alldistances.items(), key=operator.itemgetter(1), reverse=True)
    #print "==> (distance, ocurrences)"
    maxl = len(sorted_x)
    maxl = maxl if maxl < 5 else 5
    #for i in range(maxl):
    #    print sorted_x[i]

    # get factors
    #print "==> Factors"
    factors = {}
    maxl = len(sorted_x)
    maxl = maxl if maxl < 5 else 5
    for i in range(maxl):
        f = calculate_factors(sorted_x[i][0])
        #print f
        # count factor occurences
        for n in f:
            if factors.has_key(n):
                factors[n] = factors[n]+1
            else:
                factors[n] = 0

    sorted_x = sorted(factors.items(), key=operator.itemgetter(1), reverse=True)
    maxl = len(sorted_x)
    maxl = maxl if maxl < 5 else 5
    #print "==> most likely key lengths:"
    #print "(length, count)"
    #for i in range(maxl):
    #    print sorted_x[i]

    return sorted_x[0][0]

def crack(cipher, key_length):
    #
    # create groups by key length
    #
    key = ""
    groups = []
    for i in range(key_length):groups.append('')
    for i in range(len(cipher)): groups[i % key_length] += cipher[i]
    #print "==> key_length: ", key_length
    #print y
    #for i in groups: print i

    #
    # calculate frequency
    #
    letters = map(chr, range(65, 91))
    for g in groups:

        # Count letters.
        freq = dict((key, g.count(key)) for key in letters)
        #print "letter freq: ", freq

        # Compute letter frequency/probability in each group g (y_i)
        disp = dict((key, float(freq[key]) / len(g)) for key in freq)
        #print "dispersion: ", disp
        
        # Average letter occurence chances in English text. (ideal, p_i))
        english_avg = {
            'A': .082, 'B': .015, 'C': .028, 'D': .043,
            'E': .127, 'F': .022, 'G': .020, 'H': .061,
            'I': .070, 'J': .002, 'K': .008, 'L': .040,
            'M': .024, 'N': .067, 'O': .075, 'P': .019,
            'Q': .001, 'R': .060, 'S': .063, 'T': .091,
            'U': .028, 'V': .010, 'W': .023, 'X': .001,
            'Y': .020, 'Z': .001
        }

        #
        # compute table M_g => Equation #6
        # 
        ics = []
        for i in xrange(26):
            r = 0
            l = chr(i + 65)
            for j in xrange(26):
                f = english_avg[chr(j + 65)]
                d = disp[chr(((i + j) % 26) + 65)]
                r += f * d
                #print "j:",j," i:",i, " f:", f, " d:", d 
            #print "??? -> '%c' = %.3f" % (l, r)
            ics.append((l, r))
            print " %.3f" % r
        print "M_g: ", ics

        #
        # find suiting value.
        # 
        desirable = .065
        nearest_value = 999
        nearest_index = 0
        for i, ic in enumerate(ics):
            difference = abs(desirable - ic[1])
            if difference < nearest_value:
                nearest_value = difference
                nearest_index = i
        print " -> nearest: %d '%c' by %.3f" % (nearest_index, ics[nearest_index][0],ics[nearest_index][1])
        key += ics[nearest_index][0]

    return key

def main(argv):
    description = "Vigenere Breaker"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', metavar='in-file', type=argparse.FileType('rt'), help='the file to process', required=True)
    parser.add_argument('-s', metavar='gram_sz', type=int, help='the gram size', default=3)
    args = parser.parse_args()

    # get all ciphertext
    cipher = ''.join(args.i.readlines()).rstrip().upper()

    #(ic,kl) = friedman(cipher)
    #print "==> friedman test: ", ic, " kl: ", kl

    key_length = kasinski(cipher, args.s)
    print "kasinski key length: ", key_length

    keyw = crack(cipher, key_length)
    print "Key: ", keyw

if __name__ == "__main__":
   main(sys.argv[1:])
