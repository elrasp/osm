"""
Collection of regular expressions and other constants to be used
"""

import re
import string

# flags to be used for the regular expressions
RE_FLAGS = re.I | re.MULTILINE | re.DOTALL

# regex to find multiple letter repetition
RE_REPLACE_MULTI_LETTER = re.compile(r'(.)\1{2,}', flags=RE_FLAGS)
TAG_MULTI_LETTER = r'\1\1\1'

# regex to find an URL
TAG_URL = " URL "

# regex to find single and multiple Question mark or Exclamation mark
RE_SING_QUES = re.compile(r'(\?)\1{0,1}', flags=RE_FLAGS)
RE_MULT_QUES = re.compile(r'(\?)\1{1,}', flags=RE_FLAGS)
RE_SING_EXCL = re.compile(r'(!)\1{0,1}', flags=RE_FLAGS)
RE_MULT_EXCL = re.compile(r'(!)\1{1,}', flags=RE_FLAGS)

TAG_SING_QUES = " SINGLE_QUESTION "
TAG_MULT_QUES = " MULTIPLE_QUESTION "
TAG_SING_EXCL = " SINGLE_EXCLAMATION "
TAG_MULT_EXCL = " MULTIPLE_EXCLAMATION "

RE_MULTI_MIX = r'(' \
                           + TAG_SING_EXCL + '|' \
                           + TAG_SING_QUES + '|' \
                           + TAG_MULT_QUES + '|' \
                           + TAG_MULT_EXCL \
                           + '){2,}'
TAG_MULTI_MIX = " MULTI_MIX "

# regex to find negations
RE_NEGATION = re.compile(r'\b('
                         r'shouldnt|'
                         r'couldnt|'
                         r'nothing|'
                         r'nowhere|'
                         r'wouldnt|'
                         r'havent|'
                         r'doesnt|'
                         r'arent|'
                         r'didnt|'
                         r'hasnt|'
                         r'hadnt|'
                         r'never|'
                         r'noone|'
                         r'cant|'
                         r'wont|'
                         r'dont|'
                         r'isnt|'
                         r'aint|'
                         r'none|'
                         r'not|'
                         r'no'
                         r')\b'
                         r'|\w*n\'t', flags=RE_FLAGS)
TAG_NEGATION = " NEGATION "

# regex to find numbers
TAG_NUMBER = " NUMBER "

# regex to find emoticons
EYES = r"[8:=;]"
NOSE = r"['`\-]?"

RE_SMILE = re.compile(r"{}{}[)dD]+|[)dD]+{}{}".format(EYES, NOSE, NOSE, EYES), flags=RE_FLAGS)
RE_LOL_FACE = re.compile(r"{}{}p+".format(EYES, NOSE), flags=RE_FLAGS)
RE_SAD_FACE = re.compile(r"{}{}\(+|\)+{}{}".format(EYES, NOSE, NOSE, EYES), flags=RE_FLAGS)
RE_NEUTRAL_FACE = re.compile(r"{}{}[\/|l*]".format(EYES, NOSE), flags=RE_FLAGS)
RE_HEART = re.compile(r"<3", flags=RE_FLAGS)

TAG_SMILE = " SMILE "
TAG_LOL_FACE = " LOL_FACE "
TAG_SAD_FACE = " SAD_FACE "
TAG_NEUTRAL_FACE = " NEUTRAL_FACE "
TAG_HEART = " HEART "


# punctuations
RE_PUNCTUATIONS = re.compile('[{0}]'.format(''.join(string.punctuation)), flags=RE_FLAGS)