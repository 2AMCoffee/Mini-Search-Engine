from bs4 import BeautifulSoup
from collections import defaultdict
import cPickle as pickle

'''
from pymongo import MongoClient
import pymongo
'''
import os
import lxml.html
import re
import io
import sys
import math

class Posting():
    def __init__(self,docid,wf,indices,tf_idf,doc_length):
        self.docid = docid
        self.wf = wf
        self.indices = indices
        self.tf_idf = tf_idf
        self.doc_length = doc_length

    def getdocid(self):
        return self.docid

    def getwf(self):
        return self.wf

    def getindices(self):
        return self.indices

    def gettf_idf(self):
        return self.tf_idf

    def getdoc_length(self):
        return self.doc_length

invalid = ["b","c","d","e","f","g","h","j","k","l","m","n","o","p","q","r","s","t","u",
           "v","w","x","z",r"\""]
dia_wl = ["diabetes","type 1","type 2","sugar level"]
inv_index = defaultdict(list)

def tokenize(txt):
    txt = re.sub(r'[^\s\w|_]', ' ', txt)
    txt = txt.replace(u'\ufeff', ' ')
    tokens = txt.split(' ')
    tokens = re.split("[\s\n]+", txt)
    return tokens

def calcTF(wf, doclen):
    result = float(wf/doclen)
    return result

def calc_IDF(index, N):
    result = {}
    for k,v in index.items():
        for p in v:
            result[k] = 1 if result[k] == None else result[k] + 1
    for k,v in result.items():
        result[k] = math.log10(N / float(v))
    return result

def calc_TFIDF(tf, idf, word):
    result = tf * idf[key]
    return result;

if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    os.chdir('data')
    directory = os.getcwd()
    N = 0
    folder_count = 0
    idf = {}
    for i in os.listdir(directory):
        os.chdir(str(folder_count))
        cur_folder = os.getcwd()
        doc_count = 0
        docs = os.listdir(cur_folder)
        for doc in docs:
            doc_folder = os.getcwd()
            doc_name = os.listdir(doc_folder)[doc_count]
            fname = os.path.join(doc_folder,doc_name)
            print(fname)
            with io.open(fname, 'r', encoding="utf8") as f:
                corpus = dict()
                soup = BeautifulSoup(f.read(), 'lxml')
            tokens = tokenize(str(soup.find_all()))
            doc_length = len(tokens)
            tokens = set(tokens)
            kw_count = 0
            for kw in dia_wl:
                kw_count += 1
                if kw in tokens:
                    break
            if (kw_count == len(dia_wl)):
                doc_count += 1
                continue
            indexed_tokens = enumerate(tokens)
            indices = defaultdict(list)
            docid = str(folder_count) + '/' + doc_name
            for index,token in indexed_tokens:
                lower = token.lower()
                if lower not in invalid:
                    indices[lower].append(index)
            for token in indices:
                posting = Posting(docid,len(indices[token]),indices[token],0,doc_length)
                inv_index[token].append(posting)

            doc_count += 1
        folder_count += 1
        os.chdir(directory)
    print(doc_count)
    os.chdir(directory)
    for k,v in inv_index.items():
        for p in v:
            tf = calcTF(p.getwf(), p.getdoc_length())
            tfidf = calcTFIDF(tf, idf, k)
            p.tfidf = tfidf;
            print(p.gettfidf())
    print('Storing data... this might take a while')
    pickle.dump(inv_index, open("data.p", "wb"))
    print('Done')
