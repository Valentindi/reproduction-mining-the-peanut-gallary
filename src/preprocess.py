import csv
import math 
from nltk import word_tokenize
from collections import defaultdict
import os
import re
import json
import random as rd

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

data_src = "data/amazon.csv"
data_sink = "data/amazon_preprocessed.csv"
word_dict_sink = "data/count.json"
headline_dict_sink = "data/count_headline.json"

categories = [["network", "kit"], "tv" "laser printer", "laptop", "pda", ["mp3", "player"], "camera" ]
categories_simple = ["network", "kit", "tv" "laser printer", "laptop", "pda", "mp3", "player", "camera" ]

def find_in_list(categories, lst):
  #  print(categories, lst)
    if rd.random() < 0.50:
        return True
    else:
      return False


def star_bool_rating(inp, threshold=2):
    try:
        if math.isnan(float(inp)):
            return None
        return float(inp) > threshold
    except:
        print("error parsing star rating", inp)
        return None

def find_categorie(categories, title_tokenized, body_tokenized, headline_tokenized):
    c = find_in_list(categories, title_tokenized)
    if c is not None:
        return c 
    c = find_in_list(categories, headline_tokenized)
    if c is not None:
        return c 
    c = find_in_list(categories, body_tokenized)
    if c is not None:
        return c 
        
    #print("Oh None")
    return None
        

def process_line(line):
    if len(line) != 9:
        print("len", len(line))
        raise Exception("len error")

    pid = line[3]
    rid = line[2]
    ptitle = line[4]
    pcategorie = line[5]
    star_rating = line[6]
    headline = line[7]
    body = line[7] + line[8]

    found_categories = []
    found_a_categorie = False

    for categorie in categories_simple:
        found_a_categorie = found_a_categorie or str(line).find(categorie) >-1
    if not found_a_categorie:
        raise Exception("categorie error")

    bool_rating = star_bool_rating(star_rating)
    if bool_rating is None:
        raise Exception("parse bool rating error")

    ptitle = remove_tags(ptitle)
    body = remove_tags(body)
    headline = remove_tags(headline)

    ptitle = str(ptitle).lower()
    body = str(body).lower()
    headline = str(headline).lower()

    title_tokenized = word_tokenize(ptitle)
    body_tokenized = word_tokenize(body)
    headline_tokenized = word_tokenize(headline)

    rcategorie = find_categorie(categories, title_tokenized, body_tokenized, headline_tokenized)

    if not rcategorie:
        raise Exception("categorie error")

    tokens = headline_tokenized + body_tokenized

    return bool_rating, rcategorie, title_tokenized, tokens, body



with open(data_src) as ipf:
    #if os.path.exists(data_sink):
    #    os.remove(data_sink)
    with open(data_sink, "w") as opf:
        reader = csv.reader(ipf)
        writer = csv.writer(opf)
        head = next(reader)
        head = head + ["bool_rating" , "categorie" , "title_tokenized" , "tokens", "text"]
        print(head)
        writer.writerow(head)
        line = head
        continue_ = True
        it = 0
        miss = 0

        title_token_counter = defaultdict(int)
        token_counter = defaultdict(int)

        while line != "" and continue_:
            it += 1
            try:
                line = next(reader)
            except:
                continue_ = False
                continue
            try: 
                bool_rating, rcategorie, title_tokenized, tokens, text = process_line(line)
                #for t in title_tokenized:
                #    title_token_counter[t] += 1
                #for t in tokens:
                #    token_counter[t] += 1
                #print([bool_rating, rcategorie, title_tokenized, tokens])
                line = line + [bool_rating, rcategorie, title_tokenized, tokens, text]
                writer.writerow(line)
            except Exception as e:
                miss += 1
                #print(e)
            if it % 10000 is 0:
                print("it", it, "miss", miss, "found", it - miss, len(token_counter))
            
            #exit()
        print("ready")
        print("found_tokens: ", "it", it, "miss", miss, "found", it - miss, len(token_counter))

        