import re
from lxml import etree

"""
 0. prepare:
        `pip install lxml fonttools`
        
 1. download page with .otf font, for example ./fonts1/{some-hash}.otf
 1.1 fonttools util `ttx -t cmap fontname.otf`, get it's output
 2. find its font's font-family, for example "qwe_xcv"
 3. find all with it's second class(or more?), for example `.njiy_yvnk .qaz_poi`, search `qaz_poi`
 4. decode all text with that tags with `decode_char` ?
 
 There still some undecoded chars, but digits should work?
"""

dict_digits = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def get_xml_data(path):
    tree = etree.parse(path)
    return tree

# utf8 char, not bytes
def decode_char(tree, char):
    # d0 9e -> 'CYRILLIC CAPITAL LETTER O'
    str_code = str(hex(ord(char)))
    #print(str_code)
    # skip some chars
    if ord(char) < 0xff:
        return char
    # find in table
    # <map code="0x41e" name="five"/><!-- CYRILLIC CAPITAL LETTER O -->
    # selecting first table is enought?
    xpath_expr = "/ttFont/cmap/cmap_format_4[1]/map[@code = $code]/@name"
    r = tree.xpath(xpath_expr, code = str_code)
    if r:
        return dict_digits[r[0]] # can fail?
    else:
        print("can't find [{}] in xml" % str_code)
        exit(0)

tree = get_xml_data('some_hash.ttx')
print(decode_char(tree, 'О'))
