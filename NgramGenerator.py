
# coding: utf-8

# In[5]:


import nltk
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter


# In[15]:


def generate_ngrams(text):
    ph_li = sent_tokenize(text)
    li=[]
    fi=[]
    
    for tweet_part in ph_li:
        length = 3
        token = nltk.word_tokenize(tweet_part)
        for i in range(1,length):
            grams = ngrams(token,i)
            for a in Counter(grams):

                li.append(a)
    for seg in li : 
        term = ' '.join(seg)
        fi.append(term)
    return fi


# In[16]:


generate_ngrams("rodger federrer respectable sport man")

