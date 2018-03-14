
# coding: utf-8

# In[1]:


from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
wl=WordNetLemmatizer()
import re
import nltk
import string


# In[2]:


def imply_preprocess(text):
        text = re.sub('[#*@:.%&?(),!-]', '', text)
        text = re.sub('[.]*', '', text)
        text = re.sub(r"http\S+", "", text)
        nopunc = [char for char in text if char not in string.punctuation]
        text = ''.join(nopunc)
        clean_mess = [wl.lemmatize(word) for word in text.split() if word.lower() not in stopwords.words('english') and len(word)>3]
        clean_mess = ' '.join(clean_mess)
        stp = []
        stp.append(('rt','why','to','has','hv','to','is','-',';','"','amp','about','would','could'))
        
        clean_mess = [word for word in clean_mess.split() if word.lower() not in stp]
        clean_mess = ' '.join(clean_mess)
        return clean_mess


# In[3]:


imply_preprocess("I will  hv nev ad ..............get is  bored of this view from our garden #portisaac #cottagebythesea #cottage… https://t.co/jqEZ6eWezY")

