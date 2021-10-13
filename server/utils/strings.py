import pandas as pd
import numpy as np
import re
import unicodedata
import emoji
import demoji
import unidecode
import html

from textacy.preprocessing.normalize import repeating_chars
from itertools import groupby
from string import punctuation

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r"<[^>]+>",  # HTML tags
    r"(?:@[\w_]+)",  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    # URLs
    r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+",
    r"(?:(?:\d+,?)+(?:\.?\d+)?)",  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r"(?:[\w_]+)",  # other words
    r"(?:\S)",  # anything else
]

punctuation = "!\"$%&'()*+,-./:;<=>?[\\]^_`{|}~•@"

tokens_re = re.compile(r"(" + "|".join(regex_str) + ")", re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r"^" + emoticons_str + "$", re.VERBOSE | re.IGNORECASE)
control_char_regex = re.compile(r"[\r\n\t]+")
# translate table for punctuation
transl_table = dict([(ord(x), ord(y)) for x, y in zip(u"‘’´“”–-", u"'''\"\"--")])
punc = set(punctuation) - set(".")


def split_hashtag(hashtag):
    hashtag = re.sub("(.)([A-ZΑ-Ω][a-zα-ω]+)", r"\1_\2", hashtag)
    return re.sub("([a-zα-ω0-9])([A-ZΑ-Ω])", r"\1_\2", hashtag)


def explode_hashtags(tweet):
    # hashtags = extract_hash_tags(tweet)
    pat = re.compile(r"#(\w+)")
    hashtags = pat.findall(tweet)
    for h in hashtags:
        t = split_hashtag(h)
        t = t.replace("_", " ")
        tweet = tweet.replace("#" + h, t)
    return tweet


def replace_links(tweet, url_fill=""):
    """Takes a string and replace's links from with url_fill"""
    tweet = re.sub(r"http\S+", url_fill, tweet, flags=re.MULTILINE)
    tweet = re.sub(r"bit.ly/\S+", url_fill, tweet, flags=re.MULTILINE)
    tweet = re.sub(r"t.co/\S+", url_fill, tweet, flags=re.MULTILINE)
    # tweet = re.sub(r'[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)', url_fill, tweet, flags=re.MULTILINE)
    return tweet


def replace_users(tweet, user_fill=""):
    """Takes a string and replace's RT @ and @user information with user_fill"""
    tweet = re.sub("(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)", user_fill, tweet)
    tweet = re.sub("(@[A-Za-z_]+[A-Za-z0-9-_]+)", user_fill, tweet)
    return tweet


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def asciify_emojis(text):
    """
    Converts emojis into text aliases. E.g. 👍 becomes :thumbs_up:
    For a full list of text aliases see: https://www.webfx.com/tools/emoji-cheat-sheet/
    """
    text = emoji.demojize(text)
    return text


def remove_emojis(text):
    text = demoji.replace(text, "")
    return text


def split_quote_directive(tweet):
    quote = re.search(r"\[QUOTE\s(.*?)\]", tweet, flags=re.IGNORECASE | re.MULTILINE)
    if quote:
        tweet = tweet.replace(quote.group(0), "") + " [SPLIT] " + quote.group(1)
    return tweet


def remove_directives(tweet):
    tweet = re.sub(
        r"\[QUOTE_OF\s(.*?)\]", "", tweet, flags=re.IGNORECASE | re.MULTILINE
    )
    tweet = re.sub(r"\[LINK\s(.*?)\]", "", tweet, flags=re.IGNORECASE | re.MULTILINE)
    tweet = re.sub(
        r"\[IN_REPLY_TO\s(.*?)\]", "", tweet, flags=re.IGNORECASE | re.MULTILINE
    )
    return tweet


def standardize_text(text):
    """
    1) Escape HTML
    2) Replaces some non-standard punctuation with standard versions.
    3) Replace \r, \n and \t with white spaces
    4) Removes all other control characters and the NULL byte
    5) Removes duplicate white spaces
    """
    # escape HTML symbols
    text = html.unescape(text)
    # standardize punctuation
    text = text.translate(transl_table)
    text = text.replace("…", "...")
    # replace \t, \n and \r characters by a whitespace
    text = re.sub(control_char_regex, " ", text)
    # remove all remaining control characters
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")
    # replace multiple spaces with single space
    text = " ".join(text.split())
    return text.strip()


def standardize_punctuation(text):
    groups = []
    for k, g in groupby(text):
        if k in punc:
            groups.append(k)
        else:
            groups.extend(g)
    text = "".join(groups)
    return "".join(
        [
            unidecode.unidecode(t) if unicodedata.category(t)[0] == "P" else t
            for t in text
        ]
    )


def remove_unicode_symbols(text):
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "So")
    return text


def split_word_numbers(tweet):
    tokens = re.split(r"(\d+)", tweet)
    tokens = [" " + s + " " if s.isdigit() else s for s in tokens]
    tokens = [s for s in tokens if s != ""]
    return "".join(tokens)


def normalize_tweet(
    tweet,
    do_lower=True,
    do_strip_accents=True,
    do_split_word_numbers=False,
    user_fill="",
    url_fill="",
):
    # tweet = split_quote_directive(tweet)
    tweet = remove_directives(tweet)
    tweet = replace_users(tweet, user_fill)
    tweet = replace_links(tweet, url_fill)
    tweet = explode_hashtags(tweet)
    tweet = remove_emojis(tweet)
    tweet = remove_repeating_punctuation(tweet)
    tweet = standardize_text(tweet)

    if do_split_word_numbers:
        tweet = split_word_numbers(tweet)

    tweet = standardize_punctuation(tweet)
    tweet = remove_unicode_symbols(tweet)

    if do_lower:
        tweet = tweet.lower()
    if do_strip_accents:
        tweet = strip_accents(tweet)

    return tweet.strip()


def strip_accents_and_lowercase(tweet):
    tweet = tweet.lower()
    tweet = strip_accents(tweet)
    return tweet.strip()


def normalize_dataset(row):
    row["text"] = normalize_tweet(row["text"]).strip()
    return row


def remove_repeating_punctuation(text):
    text = repeating_chars(text, chars="!", maxn=1)
    text = repeating_chars(text, chars="*", maxn=1)
    text = repeating_chars(text, chars="+", maxn=1)
    text = repeating_chars(text, chars=",", maxn=1)
    text = repeating_chars(text, chars="-", maxn=1)
    text = repeating_chars(text, chars=";", maxn=1)
    text = repeating_chars(text, chars=">", maxn=1)
    text = repeating_chars(text, chars="?", maxn=1)
    text = repeating_chars(text, chars="~", maxn=1)
    text = repeating_chars(text, chars="#", maxn=1)
    text = repeating_chars(text, chars="@", maxn=1)
    text = repeating_chars(text, chars=".", maxn=3)
    return text


def explode(df, lst_cols, fill_value="", preserve_index=False):
    # make sure `lst_cols` is list-alike
    if (
        lst_cols is not None
        and len(lst_cols) > 0
        and not isinstance(lst_cols, (list, tuple, np.ndarray, pd.Series))
    ):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)
    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()
    # preserve original index values
    idx = np.repeat(df.index.values, lens)
    # create "exploded" DF
    res = pd.DataFrame(
        {col: np.repeat(df[col].values, lens) for col in idx_cols}, index=idx
    ).assign(**{col: np.concatenate(df.loc[lens > 0, col].values) for col in lst_cols})
    # append those rows that have empty lists
    if (lens == 0).any():
        # at least one list in cells is empty
        res = res.append(df.loc[lens == 0, idx_cols], sort=False).fillna(fill_value)
    # revert the original index order
    res = res.sort_index()
    # reset index if requested
    if not preserve_index:
        res = res.reset_index(drop=True)
    return res


def list_labels(x):
    return [
        x["HATE"],
        x["ANTI_REFUGEE"],
        x["INSULT"],
        x["LAW_AND_ORDER"],
        x["NATIONALISM"],
        x["RACISM"],
        x["SEXISM"],
        x["THREAT"],
    ]


def list_labels_str(x):
    return ",".join(
        [
            str(x["HATE"]),
            str(x["ANTI_REFUGEE"]),
            str(x["INSULT"]),
            str(x["LAW_AND_ORDER"]),
            str(x["NATIONALISM"]),
            str(x["RACISM"]),
            str(x["SEXISM"]),
            str(x["THREAT"]),
        ]
    )
