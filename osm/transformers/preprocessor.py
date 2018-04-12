import re

import textacy.preprocess as preprocess

from osm.transformers import constants_preprocess as const


def run_regex(regex, replace, text):
    return re.sub(regex, replace, text, const.RE_FLAGS)


def run_replace_emoticons(text):
    text = run_regex(const.RE_SMILE, const.TAG_SMILE, text)
    text = run_regex(const.RE_LOL_FACE, const.TAG_LOL_FACE, text)
    text = run_regex(const.RE_SAD_FACE, const.TAG_SAD_FACE, text)
    text = run_regex(const.RE_NEUTRAL_FACE, const.TAG_NEUTRAL_FACE, text)
    text = run_regex(const.RE_HEART, const.TAG_HEART, text)
    return text


def run_replace_negations(text, replace_with=const.TAG_NEGATION):
    return run_regex(const.RE_NEGATION, replace_with, text)


def run_replace_repeated_letters(text):
    return run_regex(const.RE_REPLACE_MULTI_LETTER, const.TAG_MULTI_LETTER, text)


def run_replace_exclamations(text):
    text = run_regex(const.RE_MULT_QUES, const.TAG_MULT_QUES, text)
    text = run_regex(const.RE_MULT_EXCL, const.TAG_MULT_EXCL, text)
    text = run_regex(const.RE_SING_QUES, const.TAG_SING_QUES, text)
    text = run_regex(const.RE_SING_EXCL, const.TAG_SING_EXCL, text)
    text = run_regex(const.RE_MULTI_MIX, const.TAG_MULTI_MIX, text)
    return text


def build_colloquial_regex_pattern(colloq_dict=None):
    if colloq_dict is None:
        raise ValueError("The colloquial dictionary is missing")
    colloq_keys = sorted(colloq_dict.keys(), key=len, reverse=True)
    return re.compile(r'\b({0})(?!\'.)\b'.format('|'.join(re.escape(c) for c in colloq_keys)), const.RE_FLAGS)


def run_replace_colloquials(text, colloq_dict=None, colloq_pattern=None):
    if colloq_dict is None:
        raise ValueError("The colloquial dictionary is missing")
    if colloq_pattern is None:
        colloq_pattern = build_colloquial_regex_pattern(colloq_dict)
    return colloq_pattern.sub(lambda x: get_value_from_dict(colloq_dict, x.group().lower()), text, const.RE_FLAGS)


def get_value_from_dict(dict, key):
    try:
        result = dict[key]
    except:
        result = key
    return result


def run_unpack_contractions(text):
    text = preprocess.unpack_contractions(text)
    text = text.replace("'s", "")
    text = text.replace("'d", "")
    return text


def run_preprocessor(text,
                     default_preprocessor=None,
                     replace_urls=False,
                     replace_emoticons=False,
                     replace_exclamations=False,
                     replace_punctuations=False,
                     replace_numbers=False,
                     replace_negations=False,
                     replace_colloquials=False,
                     replace_repeated_letters=False,
                     replace_contractions=False,
                     replace_whitespace=True,
                     replace_currency=False,
                     replace_currency_with=None,
                     colloq_dict=None,
                     colloq_pattern=None):

    if replace_colloquials is True and colloq_dict is None:
        raise ValueError("The colloquial dictionary is missing")

    if replace_whitespace is True:
        text = preprocess.normalize_whitespace(text)

    if default_preprocessor is not None:
        text = default_preprocessor(text)

    if replace_urls is True:
        text = preprocess.replace_urls(text, replace_with=const.TAG_URL)

    if replace_emoticons is True:
        text = run_replace_emoticons(text)

    if replace_exclamations is True:
        text = run_replace_exclamations(text)

    if replace_numbers is True:
        text = preprocess.replace_numbers(text, replace_with=const.TAG_NUMBER)

    if replace_negations is True:
        text = run_replace_negations(text)

    if replace_contractions is True:
        text = run_unpack_contractions(text)

    if replace_colloquials is True:
        text = run_replace_colloquials(text, colloq_dict, colloq_pattern)

    if replace_repeated_letters is True:
        text = run_replace_repeated_letters(text)

    if replace_currency is True:
        text = preprocess.replace_currency_symbols(text, replace_currency_with)

    if replace_punctuations is True:
        text = preprocess.remove_punct(text)

    if replace_whitespace is True:
        text = preprocess.normalize_whitespace(text)

    return text
