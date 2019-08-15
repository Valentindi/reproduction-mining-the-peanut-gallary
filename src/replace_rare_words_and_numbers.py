import pandas as pd
from ast import literal_eval
import re
from collections import defaultdict

data_src = "data/amazon_sample.csv"
data_sink = "data/amazon_sample.csv"

word_dict_sink = "data/count.json"
headline_dict_sink = "data/count_headline.json"
rare_word_replace="RAREWORD"
number_word_replace = "NUMBER"

def count_tokens(inp):
    lst = []
    for d in inp:
        lst += literal_eval(d)
    res = defaultdict(int)
    for t in lst:
        res[t] += 1
    return dict(res)


def get_rare(counter, threshold):
    rare_words = [w for w in counter if counter[w] <= threshold]
    return rare_words


def repl_one(rare_words, d):
    d = literal_eval(d)
    for it, t in enumerate(d):
        if t in rare_words:
            d[it] = rare_word_replace
    return d

def repl_numbers(d):
    d = literal_eval(d) if type(d) is str else d
    for it, t in enumerate(d):
        t = number_word_replace.join(re.split("\d+?\.\d+", t))
        t = number_word_replace.join(re.split("\d+", t))
        d[it] = t
    return str(d)

if __name__ == "__main__":
    df = pd.read_csv(data_src)

    print("replace repl_numbers")
    df["tokens"] = df.tokens.map(repl_numbers)
    df["title_tokenized"] = df.title_tokenized.map(repl_numbers)

    print("count tokens")
    token_counter = count_tokens(df.tokens)
    headline_token_counter =  count_tokens(df.title_tokenized)

    rare_tokens = get_rare(token_counter, 10)
    rare_title_tokens = get_rare(headline_token_counter, 10)

    print("replace tokens")
    df['tokens_no_rare'] = df.tokens.map(lambda d: repl_one(rare_tokens, d))
    df['title_tokens_no_rare'] = df.title_tokenized.map(lambda d: repl_one(rare_title_tokens, d))
    df.to_csv(data_sink)
    print("ready")