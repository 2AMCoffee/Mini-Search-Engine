from __future__ import division
from collections import defaultdict
from create_index import Posting
import os
import cPickle as pickle
import json
import math

if __name__ == '__main__':
    os.chdir('WEBPAGES_RAW')
    with open("data.p", "rb") as f:
        data = pickle.load(f)
    corpus_size = len(data)
    query = ''
    while(True):
        query = raw_input('Please enter a search query: ').lower()
        words = query.split()
        if words[0] == 'quit()':
            break
        scores = dict()
        query_scores = []
        for term in words:
            lower = term.lower()
            if data[lower]:
                score = 1 + math.log10(1) + math.log(corpus_size/len(data[lower]))
                for doc in data[lower]:
                    current_doc = doc.getdocid
                    scores[doc.getdocid()] = (doc.gettf_idf() * score) / doc.getdoc_length()
                        
        postings_list = []
        
        for k,v in sorted(scores.items(), key=lambda t:t[1], reverse=True):
            if (len(postings_list) == 10):
                break
            print(k,v)
            postings_list.append(k)
            
        result_list = []
        with open('bookkeeping.json') as json_file:
            lookup = json.load(json_file)
            for posting in postings_list:
                result_list.append(lookup[posting])
        for result in result_list:
            print(result + '\n')
