
# coding: utf-8

# In[57]:


import string
import pandas as pd
import requests
import json
import TextPreprocessor as tp
import ImpliedPreprocessor as ip
import NgramGenerator as ng
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


# In[58]:


st = StanfordNERTagger('C:/Users/Admin/Documents/DS/stanford-ner-2017-06-09/classifiers/english.all.3class.distsim.crf.ser.gz',
					   'C:/Users/Admin/Documents/DS/stanford-ner-2017-06-09/stanford-ner.jar',
					   encoding='utf-8')


# In[59]:


import os
java_path = "C:/Program Files/Java/jdk1.8.0_25/bin/java.exe"
os.environ['JAVAHOME'] = java_path 


# In[3]:


def microsost_ngram_service(list_of_segments):
    key_phrase_api_url = text_analytics_base_url + "keyPhrases"
    subscription_key="e494891061104f4cabe601316fac1a5b"
    assert subscription_key
    i= 1
    lstnew=[]
    for text in list_of_segments:
        dicton={}
        dicton['id'] = i
        dicton['text']=text
        lstnew.append(dicton)
        i=i+1
    documents={}
    documents['documents']=lstnew
    headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
    response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
    key_phrases = response.json()
    final_list = key_phrases.get('documents')
    newColList=[]
    for a in final_list:
        if len(a['keyPhrases']) == 1:
            term = a['keyPhrases'][0]
            newColList.append(term)
    return set(newColList)


# In[62]:


# def give_top_utility_score_features_new(tweet,corpus,local_ner_corpus):    

# #     import os
# #     java_path = "C:/Program Files/Java/jdk1.8.0_25/bin/java.exe"
# #     os.environ['JAVAHOME'] = java_path    
# #     list_of_segments = ng.generate_ngrams(tweet)
#    tfidf = TfidfVectorizer( stop_words='english',ngram_range=(1,2))
# #     messages_bow = bow_transformer.transform(corpus)
# #     tfidf_transformer = TfidfTransformer().fit(messages_bow)  
# #     tfidf = TfidfVectorizer( stop_words='english',ngram_range=(1,2))

#     tfs = tfidf.fit_transform(corpus)
   
#     response = tfidf.transform([tweet])
#     feature_names = tfidf.get_feature_names()
#     for col in response.nonzero()[1]:
#         print(feature_names[col], ' - ', response[0, col])
#     #print("give :" ,bow_transformer.vocabulary_)
#     rlist=[]
#     list_of_ners=[] 
#     global_microsoft_list_of_ngrams=[]                                 
#     tokenized_text = word_tokenize(tweet)
#     classified_text = st.tag(tokenized_text)
#     filteredList=filter(lambda x:  x[1]!='O', classified_text)
#     filteredList = list(filteredList)
#     #print(l)  
#     if filteredList :
#         for objects in filteredList :
#             list_of_ners.append(objects[0])
    
#     global_microsoft_list_of_ngrams= microsost_ngram_service(tweet)
  
#     #ngram_corpus=set(ngram_corpus)| microsoft_list
#     for ner in list_of_ners:
#         if ner not in local_ner_corpus:
#                 local_ner_corpus.append(ner)
#                 weight_of_ner=1
#         else:
#                 weight_of_ner=2 
                
#     for ngram in global_microsoft_list_of_ngrams:
#         if ngram not in feature_names:
#             weight_of_ngram=featues
#         else:
#             if(features_names)
#             weight_of_ngram=2
   
        
        
           
#     return (local_ner_corpus,ner_corpus,microsoft_list)


# In[63]:


# give_top_utility_score_features_new("cinema fgfgfjkh",[" would","would","bigdata "," hjgjh"," would"," would"],["Sachin"],["hey dhoni"])


# In[4]:


def initialisation(list_of_collected_tweets):
    local_ner_corpus=[]
    corpus=[]
    for tweet in list_of_collected_tweets:
           
            tweet=ip.imply_preprocess(tweet)
             
            tweet=tp.clean(tweet)
             
            corpus.append(tweet)
             
            tokenized_text = word_tokenize(tweet)
            classified_text = st.tag(tokenized_text)
            filteredList=filter(lambda x:  x[1]!='O', classified_text)
            filteredList = list(filteredList) 
            if filteredList :
                for objects in filteredList :
                    local_ner_corpus.append(objects[0])
    return (local_ner_corpus,corpus)            


# In[2]:


def give_top_utility_score_features(tweet,corpus,local_ner_corpus):
    final_segments={}
    local_weight=0
    global_weight=0
    final_weight_for_segment=0
    list_of_segments = ng.generate_ngrams(tweet)
    tfidf = TfidfVectorizer( stop_words='english',ngram_range=(1,2))
    tfs = tfidf.fit_transform(corpus)
    #local_ngrams
    response = tfidf.transform([tweet])
    local_list_of_ngrams = tfidf.get_feature_names()
    local_ngrams={}
    for col in response.nonzero()[1]:
        local_ngrams[local_list_of_ngrams[col]]= response[0, col]
    #print(local_ngrams)
    
    
    #local_list_of_ngrams=list(set(local_list_of_ngrams))
    #global_ner
    global_list_of_ners=[]                                
    tokenized_text = word_tokenize(tweet)
    classified_text = st.tag(tokenized_text)
    filteredList=filter(lambda x:  x[1]!='O', classified_text)
    filteredList = list(filteredList)
    if filteredList :
        for objects in filteredList :
            global_list_of_ners.append(objects[0])
            #global_ngram
    global_microsoft_list_of_ngrams=[]  
    try:
        global_microsoft_list_of_ngrams= microsost_ngram_service(tweet)
    except:
         pass
    for segment in  list_of_segments:
            final_weight_for_segment=0
            if segment in global_list_of_ners:
                global_weight+=0.3
            if segment in global_microsoft_list_of_ngrams:
                global_weight+=0.3
            if segment in local_ner_corpus:
                local_weight+=0.3
            if segment in local_ngrams:
                local_weight+=local_ngrams[segment]
            final_weight_for_segment=((global_weight))+(local_weight)  
            #print(segment," : ",final_weight_for_segment)
            if (final_weight_for_segment >=0.3):
                        final_segments[segment]=final_weight_for_segment
            #print(segment," ; " , final_weight_for_segment)
#             new_final_segments = dict(sorted(final_segments.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
            
    new_final_segments=sorted(final_segments,key=final_segments.get,reverse = True)[:5]
    #print(new_final_segments) 
    new_final_segments=new_final_segments+list(global_list_of_ners) + list(global_microsoft_list_of_ngrams)
    #print(new_final_segments)    
    tweet=tp.clean(tweet)
    tweet=ip.imply_preprocess(tweet)
    corpus.append(tweet)
   
    local_ner_corpus=set(local_ner_corpus) |set(global_list_of_ners)

    return (new_final_segments,corpus,local_ner_corpus)
            


# In[65]:


# testing=[
#          'IPL is about to begin',
#          'Entertainment is important',
#          'rodger federrer is a respectable sports man',
#          'Football is a interesting game',
#          'Aishwary turns 42 this november',
#          'Dhoni is about o quit from IPL' ]


# In[68]:


# local_ner_corpus=[]

