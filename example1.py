#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crack Vigenere
~~~~~~~~~~~~~~

Searches for the key (length must be given) to a text encrypted
with the `Vigenere cipher`_.  Cracking works by analyzing the
frequency of occurences of letters.  When the keyword is found,
the cipher is decrypted.

I'm not sure if it's absolutely correct, but it succeeded in
solving my tasks.

:Copyright: 2004-2008 Jochen Kupperschmidt
:Date: 11-Apr-2008
:License: MIT

.. _Vigenere cipher: http://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
"""

from collections import defaultdict
from itertools import chain, imap, izip


# Average letter occurence chances in English text.
p = {
    'A': .082, 'B': .015, 'C': .028, 'D': .043,
    'E': .127, 'F': .022, 'G': .020, 'H': .061,
    'I': .070, 'J': .002, 'K': .008, 'L': .040,
    'M': .024, 'N': .067, 'O': .075, 'P': .019,
    'Q': .001, 'R': .060, 'S': .063, 'T': .091,
    'U': .028, 'V': .010, 'W': .023, 'X': .001,
    'Y': .020, 'Z': .001
}

def crack(cipher, m, details=False):
    """Crack."""
    cipher = cipher.upper()

    # Split cipher.
    y = defaultdict(list)
    for i, char in enumerate(cipher):
        y[i % m].append(char)

    # Analyze sections separately.
    for si in xrange(len(y)):
        section = y[si]
        section_len = len(section)

        show_headline('section %d' % (si + 1))
        print wrap(section)
        print ' -> length: ' , section_len

        # Count letters.
        c = dict((key, 0) for key in p)
        for char in section:
            c[char] += 1

        # Compute letter dispersion.
        h = dict((key, float(c[key]) / section_len) for key in c)

        # All the magic happens here :)
        gs = []
        for g in xrange(26):
            r = 0
            letter_g = chr(g + 65)
            for i in xrange(26):
                p_i = p[chr(i + 65)]
                h_ig = h[chr(((i + g) % 26) + 65)]
                r += p_i * h_ig
            if details:
                print " -> '%c' = %.3f" % (letter_g, r)
            gs.append((letter_g, r))

        # Fetch best suiting value.
        desirable = .065
        nearest_value = 999
        nearest_index = 0
        for i, g in enumerate(gs):
            difference = abs(desirable - g[1])
            if difference < nearest_value:
                nearest_value = difference
                nearest_index = i
        print " -> nearest: '%c' by %.3f" % gs[nearest_index]
        yield gs[nearest_index][0]

def decipher(cipher, keyword):
    """Decipher the text using ``keyword``."""
    cipher = cipher.upper()
    keyword = keyword.upper()
    keyword_values = map(ord, keyword)
    keyword_len = len(keyword)
    for i, char in enumerate(cipher):
        char = ord(char) - keyword_values[i % keyword_len] + 65
        if char < 65:
            char += 26
        char += 32  # Lowercase; this way instead of `.upper()`.
        yield chr(char)

def show_headline(title, width=47, fillchar='='):
    """Display a formatted headline with fixed width."""
    beginning = (fillchar * 3) + ('( %s )' % title)
    print '\n' + beginning.ljust(width, fillchar)

def group(iterable, n, padvalue=''):
    """Group ``iterable`` into chunks of ``n`` items.

    The last chunk is padded with ``padvalue``, if necessary.
    """
    return izip(*[chain(iterable, [padvalue] * (n - 1))] * n)

def wrap(string, blocks_per_line=8, block_width=5):
    """Wrap long lines into cute little blocks."""
    blocks = imap(''.join, group(string, block_width))
    lines = imap(' '.join, group(blocks, blocks_per_line))
    return '\n'.join(lines)

def main(cipher, kw_len):
    print 'Cracking the Vigenere cipher.\n'
    details = (raw_input('Show details? [y/N] ') in ('y', 'Y'))
    show_headline('cipher')
    print wrap(cipher)
    print ' -> assumed keyword length:', kw_len
    keyword = ''.join(crack(cipher, kw_len, details))
    show_headline('deciphered')
    print wrap(decipher(cipher, keyword))
    print ' -> keyword: "%s"\n' % keyword

if __name__ == '__main__':
    # Example 1
    cipher = 'KCCPKBGUFDPHQTYAVINRRTMVGRKDNBVFDETDGILTXRGUDDKOTFMBPVGEGLTGCKQRACQCWDNAWCRXIZAKFTLEWRPTYCQKYVXCHKFTPONCQQRHJVAJUWETMCMSPKQDYHJVDAHCTRLSVSKCGCZQQDZXGSFRLSWCWSJTBHAFSIASPRJAHKJRJUMVGKMITZHFPDISPZLVLGWTFPLKKEBDPGCEBSHCTJRWXBAFSPEZQNRWXCVYCGAONWDDKACKAWBBIKFTIOVKCGGHJVLNHIFFSQESVYCLACNVRWBBIREPBBVFEXOSCDYGZWPFDTKFQIYCWHJVLNHIQIBTKHJVNPIST'
    kw_len = 6

    cipher = 'cpimvtcmngiheycgremhwltmvtceiiqwivwhmumhwptawgoptfizftgitlezpcgxfspsbuchhbqwhalhdsaosxyceispdtbxoetzwtsmcgjoyoiseggpdwxzalstddwimwrlltbsahrgxnaedwtlhgdahrhwpfkovxeghdqtasrcimwpdhtgvtvxbqtrmvizapcgwdyobzultxntbccdevccoogzntnbaezrmocnemcisemoapoyhgzytbsehxztregrdqakhwfrtbstsloxoaloulcmhdsaosxysiwgpdlcbpoyhwpetfajntjxramcgdoyhwpsblipeghwneghjcymvxdmrhwtctzillxcuhhbqwehxgjmjxqihalowtsmcgjoyhwpwtfhzfmvtltasctaggprabbhetasxdltbszfthalnmwhtslieaolsseousuzugrtouicclnnbutnbgwpdictxoygdwoghdhhbqwttpcjwdaokpsmcdoighwpstatceeoitogohehxkgttbbvdoyhwplhudrrtdwprlhdehxddpmlcusofsgttpcjwdaokpthzszftgicuzuapfhfatbxfijcihxxightydxrizrxdgpsxbiehxqdyfewreoydtcsbopydasawalktxarxjogxtgzmmvtyouztnofatycxatythtisemwblengucofhwpfkovxeghdqtasrcimwpdimgtwftbsqrhaisemvxcducdvoyhwpltkhtnpvpemtbcprizpeopcjwdaokptkspeewhwtsawvsakujxeghlpctbdylrujpslkwjtasvcethspsbuchaloqlnwccpdisgsaigqpctihppeoizbxqpxelscdiuztzflcbpigqdygkixeybbpqivhxeihihsilhdcyhfqpctihphxvpolhgisilwceeksheigwizrusrlulspovtbrtnzmtlrltdcbtrtehxqdxpesitogcutttbshefonalxohponfhploshhimviseyocnymvpehtrisilwblgbbpcygogcamwkpeosgmexbutnbgwpdpshsonzssaosuzugrewamcwtmlsaqsraeltawhtnzkxehmvtdtkivrlxtdchxzapnbqxydxdtydxbrpcizphslwcrigupsyfbdqtkwjxpackprfogltacclnwgpwafwhaekvpasfoztnzhwprxtapcmwdyoyvtcowcifspvtceasrznmsbalthtdtasvcophwzfmvtltasctagsbaikswzwufpgethwtnzwhqrxsszmhthaexqwhhbqwsalapoemvtltasctagghzftfticxsspvxfnztasgdtthtzfasawalwcrrxoiyelgdcmhftarhppmlroierbpjeiguiseowreokmiztaspycbsceghcszrwsgzfthwpnlocothhwpftjdcoyoezlecpydthwpnxqetnmfdothqgttbohlgtwcalthdxarptcezogoewohehxqpattwclraqwpghndclxosprhtprohrajbtbszfycawopsgdfhfxytasgppnpatcbgizbxtdfnwhwpokwvtntzdqcbqtcolrtceiiqwivodqsmojrulhxyelqxeyhtvzdhtisenhdaitcudikhwzmtgbzrxocooyhwpnnatcongdehxfxxazwclrrgiltxglsivvpceyfpxewieznmvtdafsbzdxzisexlipnmhdhhbqwlrbgiztesdctaspcilhdeeewpysvvdzlpsgpigrtmtxrizhbaxytasezlbhxnsaohmexbattmztcevcvyilsslnwhwprxqdrnbhxznbgisefcgpnxqtdstfnmevojdebhxdnhhbldxpnlrbgizteswtmlsaqtasihoivxwolcesekgwldfcgpigqdxmhbisaghwpypsgpchbhnihihzftbsarhppmlrgdxexztxeghhzfizpeoksbliggitleicoemsreewwclrbgiztesxyeguatsadwtlhgdahrhdzmtbnlfywcttbshxarptertqtonhhdylrwcehxkdcklcuehxqpxbkwsreizpeogwhesuiitnzftlthfxrigoahrbhtcsewzpbxfzplxmdcchztciwuteoizpeotbssilwspalhwltmvtcebgpernhwsizvtctaocpxisgtegqtzfpvxnhmvtxigrqpakglttgshdthvtcsxzutstqdyvbqitogkwtcawczukclygxbtcamwdyhtgqpegscehngxlsmwrllempdsxfipdtbstsisgsaigvligwcrgkcjydhtisezftpktiisokglsothiseksclilgpycxpgzuzvilnxkatfxwceomvthokzsalthdsalvpotasvcethtdtbbuwuxbrptasgppnpatchtewamcxdaegdehxtxcsmhgpamwhpuiccpdnqpeihbdqwawrstaslcimwcrshtbtlmcclnwzdnkxfdfslspfjxocaanzpydzctehxogptasapgbhxxamsspsvscoaghhwidsslnmsdcbnbnlnaswlstftgeeoitogculnhhwprewuplbytmavccsebgecoycjydemxxpkshdewkxehmvtfnbhnzfdbdhlxrvpighwpetfajcaignhastiekqxdewogpaewcqlnscnehbisehzdrytbsltmvtceowkllhtattxfpeuksdyphzxeivgtgeghwpfkovxeghhzfawhhokrhhhxbgppxoipdthhpchbssagrhjmivpgebbpwltutdrtjxdhxriseaspctlcuxegkwzhtjtdexbgpfesreewwcehxaisebfdhnawvsekbpeukswpilhwpfthwprhtxoetzxdmbbesiechzpamxyphzxeivgxylbhtcamigpagrblnrcuehxzpeelhrznvseeihbhzffcsprghwtndsgdagrheamshxeggjnhtgisenbxeyhtzyopztogxhwprxwvyoyzphagrisexejllbhnzfmvtdeqshsaosqpegoceivweltxrxyawftlmumwtmmvtlrzibpnmcuehxftauuzxnilhwpsxognhttiprciheivsisegoifrxcuhhbqwtsywgdtawceewoimyvsesaeihehxxjdttbsmltatwelgdwdfocehxbstsvihdewccehxppdilcuarhjtcbboaxokoattrpndovfpeelocophztxakqwfsmvtyctfxnamigpdumisrtgnxavvjdagrelrmwpwlrsmaltwcpdumhzckoipskssfcxrizagoqdtkoreihbqjgeojnogocoawsxxaghjdagrwlvbbvmevcbpigjxdiuzttnmvttnwwktdnoacetdepakgpelxbvehbbisebrtlllhpeepvxnhbgrznlhgfcmssmylcrcamshehxtxcsmqpcehtisekiaprlwheoustouvoitogcuhhbqwlnhiiwigsxddkolyayhtctasdwdasawegwrxowsaarhjxoigudylrtdcagwbarhjtorxzxrihbpydfcgllbhnlnwadcelwbalbqxeybbbfsbqpydzmbyalhxnafocwixfhertwczficterrocogkspeekvpcmhbnzfmvttnwwktdnoalnwhwpsmoipwxogptaihwewcceomvtnogqtatbcczftvxrhxfheamsxywawrsnhapyctzadagmisiguwtshkclnwwchhbqwehxfttsgsxehxfblrkmxyggcgriowcrigapcrbovpagrztnzgpceivxwolcesekgpydivxwolcesekgpcedwcrstbsehxfttstbdehxfpydawvsekssfcthxznbbiplesreutzpdwxzalsfcglltbsceewvtongdqsvwtycxohheezpdoyogeagrczthtnzumvdylrpjeoyhwpwacapoyzxqelirsalhpeebgwlrwzneousgpaewopdbbisilkdclwocoqnwrvlrrtregsgltxgiztaseprysreiwspwsnqrpewgisezckprgatythtiselcaoixfpydmvtwoosgzfacczukhwtstuptnwsrwigwcrighdoefcrcavmpydwsbzckorjighdeykocyybbpyifovtntfnmumftrueogzrwsgsaowcrnhhbfcaftdefpalnvsiztaspntnoaqavhhhhxbisepvtplaohnofsufleqxcceslpdhbdebxuxyazoxywbhwlnxkeprbcszfaiblnewupbnhlphtjtaalgtofkcbehxptdtmcisepcgdttbsehxfthexbsehxgjmjxqitsmvtycaocrewocotasdwdjipcrxzdqphsicytbsahbzddoivnhhbqwsawptpnfcgplbuwelrhgpamsstnmvtpakzxprucdvshtiseksefbewrtsgclcelibpdtbsqonuweonhizavccnlngxznicterrwhoilqdgeksseouspyifwiltbccehkwrprxadgewtgzmmvternhwlnwvdxekohheezpdtasscafoitcictesaoktnzptpnvccoefbtoaloctmbhpeokwhdeghxythppyilvbpnmoaznzkxehmvtxagrisebrtloyhwpsmoipilgjapesbpnmssmymvtceosaltbcczfttjeuksatfxhwpdbjxdihbxythpdzklzxvetzadifwalrwwktsbccdcigxcgvzthilwcehxqalslwrllfihpufwharhppmlrzpeekhwlnmvtlgxcualthdehxbpeukoaoiowhtoggpceywkpigbjxbxfqzodwpydmvtqikgisaetdqbhcztiwclythhwpptfprrtdwmezwcyiguxsawoahargpombftotasvpnbihzfzzpfchbpydtrttmtbifspvxnhbgxytkcsfcmcgjtasutrlhqzodqdyttwctnzogpfnhpeihbdqtasezpnzpcagrhzpawheivoayomwdyshtyfsmwrpagrrznvzjoiguatkxgdxehtisexogwixfstaecvfelkxehhiilrkwktnzoilnrrtqigwiprxgjwtmcisilwhlpiscoewogpsmoipmxbizfmvtyamigpoyxjdtbqtlcvcgoiguizchabznhdxyihbpydtbpyspsgtswsblnwsseomvtbuxgitogkwltbgyfsmwrpsmfxapxrdqaidtlrtbrpsmvtdevccodbjxdihbxyceispsmvtcefoxydxfdqtashpchbslnwhwpwacapoyhwptawgoagruzukhwmohyhhhbqwlrxaptnemdncndxpdpwistasrznlhgfcmwdyoyhwpfbfhesmoipagriseywgdtxrjnamwdytasisikrstvbgxznvccdilhhzfmvtqiyhwdiqhwlnwgtgeghwmohyhtnpvxnhivxwolcesykoisekhwlnciheivsxdtashfbcsreoyscbubfnlnwhwpsxqdydlhpeebgrznlhgfcmssznifxycbdapshtrzmfictsfocornztobrdwtlhgdahxfhlnwhwpchbipmizpeihbdqtasxoetcurohrilkxgiseizpnehtiselcrtaeocophzxeivoagikhjpsbbisexwvstaoconbbisbhczdtaseprosgdihbhzflhpeelocooyhwpigrxgiwipwspvdnokftdphbseomvtxaksgpvbslpdbbhfcvshdihbpydmvtyamigpoydapaligpagriseifxycbdapoyhncagbnlrxtjctasglntzndewwcehxwcoiowsfaeapytasipnmvqzodwhehxqdyceihtogcuehxkwzlxwchhbqwehxftwamwdyshtesiechzpamizphsicytftqigoawywsiprfwcpdtbsehxvpapbbtdshtisevwitzxbhtnmvxdlbtthhbqwsalbdhbxsclsligpdbgrcopbtobrhwpvbgxznhtpyomvtcokobzrxutyekoaoiowhtogwceomkdaakhhxarptldhdipdmvtqikgimohyhtioqdyttwctnzhwpdxgrciihxznhtpdtthtqrtatogxbtcaezntntqrzrwocnepwishxzapnbqcztbccdoyftwizwdyagrbzrtzxeypvxwebbiselsrznwpdzkljmehxvtwlxbxnsmoipilhglnltdcmxrxythoctdxoaviguszmhtesiechzpamdqwawrsaezdehxfvzvxfcxeghhlrxhwppxfkprlwdysmvtdemkdaobbidoyjxpwtftcetzajoidddewocotasdaphgxeihbxdogzngebztobrhwpgxbxfshtewamciseksefbewrwidsiseivppdkihdexwcerhrjntbcceoivppdkihtstbxxpxfupcmkwzlxhwphbuwprewvsthtesiechzpamqcetyhehkcjrhmvtcezialrbhnzfmvtseeztyivhtxpeslsivvpeltgiqawshlwtmxythhwphxokpnlkwptasgehbgxxpxfupcmwdyoygicuvhjcetfxdeltgzmtbtyltfvpmxbizfmvtaltbdcfkcbehxwbaekttntksrznvwapmxbitnmvthrbhtcshkcxigrdqtashernuvwigutwefsceshtisonuwewawrsaksczwywgdtufdfgahizgxhwprumwtmhfepraoedfkcbehxqdxphgxeihbdqtaslzrdoioiyttceghitmxgpcejitdtbccdlbytehxgxxieogbuxgitogoqzumhwpiewpoagrisehrndsxmlsivvpcepcgehtgztnzpjewawrsctbcztaokpawwheigqilnlktcighwpazsdqpeoiztasgpwtgczrxujwakadoehtefbewrltbcclnwoclumvdcwhiaohtjtehxztdslqgfpesxyaehtcigudcawrxygmcphokylsivvllsdbdhnhbajthoupwhtwtsyfxpnwgiseksxdnhoqdukrxeybbhfpichtnzhwltasblyaokpltwssilzpmonfhlsbrtqokoitmxcgeukbtofkcbznxkdckmcpyomvtcagrhfcawceekfjatbccdwhiaobxadceewzplrhdzcvigtnmvtnalsdqaeccrtaoczftgwzrmkgttbbvtntzaltmsbatlhdoemsgxigsisevvgznhzdrivoazrwsgzfmvtalthdyivkgttbbvdogwceekbpweowspnvsisilicnekhptnmmpmonhpyylwcrlxrxllhujpbxwcrchaezsxrpeogsitmxwhldbgifruwcreesbpnmkwtcaajdtuspombhipdmcpqfxqiwogutcwhfzdsnqwlsmvtceiiqwivocotasalwladcemvpysacgeekccpsuiiznmvtztasgsagriselstxigustsvftaagqxpshtiseksefbewrxarccwytfxdehiizfmvtoilqdcdtbiplxatytlkwtcahwppawazshdwpraohltmsbatxrizugwipigohtnzzthhhztaekvpaspwisonhqpiguwtmlsaqauzteoksrzggwhptasxychbhtsmscnypvxnhbgdmvbcjdthihqokhwprxwhljnrvxeghdqayhtcazshhhbqwqepugpamkgttxfhsaostgekptpntpapthoceivweltxtdctasbdeejtdtasnoogciaekqttvxhwpwtbizfvccyeqwdyighwpikclywkwitnzgdctasvlplwcehxwgdylhtxspvxnhtftgilwqwexbdfgahdehhgthhhqdxettiprmvtxighwpbxuxynbbvdoyzxeekoifrxocopawazshdwjafwsehxtxcsmsuqokhhzfmvdfgahpydeocrututxoksxychbhtsmscnixgdncnfisagbdhwascehxdpehlcudpxqjwamwdyakslplekdcntbsehxatlnbbvzfpcgosiftnilsajdxtxyewtdcchbhtsmscnymcdtsmvtrrhkisoyhxxetbsdofsdqtasvcethtdtvftltbccdoyhwphnapymbbssaosqpegkpytbbvtnnbxeymfxpdumisilhtdtlskprtzdqtasewamcctcwwpwozitdavqdcdbbveohigxowsgyiwspdaidtlrmcqpdxttntbjtmumhwpdxtxnixbrjilbdarhcuehthiserktcevcbaolssltwwuqekscetbatdokpnoiyttceghwlnwgpydmvtduidddimwdytaoiehxftauuzxnwtglcimhtyugwceekfjatxrajagrqjavcceigidfsxtuzrmwhtnlcbpdxugpevccqikatobrhwpnnatconggpfxftycxgucofccpptfizfmvthokyizagcisek'
    kw_len = 5

    # Example 2
    ##cipher = 'CHREEVOAHMAERATBIAXXWTNXBEEOPHBSBQMQEQERBWRVXUOAKXAOSXXWEAHBWGJMMQMNKGRFVGXWTRZXWIAKLXFPSKAUTEMNDCMGTSXMXBTUIADNGMGPSRELXNJELXVRVPRTULHDNQWTWDTYGBPHXTFALJHASVBFXNGLLCHRZBWELEKMSJIKNBHWRJGNMGJSGLXFEYPHAGNRBIEQJTAMRVLCRREMNDGLXRRIMGNSNRWCHRQHAEYEVTAQEBBIPEEWEVKAKOEWADREMXMTBHHCHRTKDNVRZCHRCLQOHPWQAIIWXNRMGWOIIFKEE'
    ##kw_len = 5

    main(cipher, kw_len)