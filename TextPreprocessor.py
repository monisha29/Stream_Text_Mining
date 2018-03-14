
# coding: utf-8

# In[6]:


import re
import sys
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
wl=WordNetLemmatizer()

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)
opts = {
    'URL':'urls',
    'MENTION':'mentions',
    'HASHTAG':'hashtags',
    'RESERVED':'reserved_words',
    'EMOJI':'emojis',
    'SMILEY':'smileys',
    'NUMBER': 'numbers'
}
Options = enum(**opts)
Functions = enum('CLEAN', 'TOKENIZE', 'PARSE','IMPLY')

class Patterns:
    URL_PATTERN=re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
    HASHTAG_PATTERN = re.compile(r'#\w*')
    MENTION_PATTERN = re.compile(r'@\w*')
    RESERVED_WORDS_PATTERN = re.compile(r'^(RT|FAV)')

    try:
        # UCS-4
        EMOJIS_PATTERN = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
        # UCS-2
        EMOJIS_PATTERN = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')

    SMILEYS_PATTERN = re.compile(r"(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}", re.IGNORECASE)
    NUMBERS_PATTERN = re.compile(r"(^|\s)(\-?\d+(?:\.\d)*|\d+)")



class Defines:
    PARSE_METHODS_PREFIX = 'parse_'
    FILTERED_METHODS = opts.values()
    PREPROCESS_METHODS_PREFIX = 'preprocess_'
    IS_PYTHON3 = sys.version_info > (3, 0, 0)
    PRIORITISED_METHODS = ['urls', 'mentions', 'hashtags', 'emojis', 'smileys']
 




    
class Preprocess:

    tweet = None

    def __init__(self):
        self.repl = None
        self.u = Utils()

    def clean(self, tweet_string, repl):

        cleaner_methods = self.u.get_worker_methods(self, Defines.PREPROCESS_METHODS_PREFIX)

        for a_cleaner_method in cleaner_methods:
            token = self.get_token_string_from_method_name(a_cleaner_method)
            method_to_call = getattr(self, a_cleaner_method)

            if repl == Functions.CLEAN:
                tweet_string = method_to_call(tweet_string, '')
            else:
                tweet_string = method_to_call(tweet_string, token)

        tweet_string = self.remove_unneccessary_characters(tweet_string)
        return tweet_string
    
    def imply_preprocess(text):
        text = re.sub('[#*@:?(),]', '', text)
        text = re.sub(r"http\S+", "", text)
        ps=LancasterStemmer()
        clean_mess = [wl.lemmatize(word) for word in text.split() if word.lower() not in stopwords.words('english')]
        clean_mess = ' '.join(clean_mess)
        return clean_mess
    

    def preprocess_urls(self, tweet_string, repl):
        return Patterns.URL_PATTERN.sub(repl, tweet_string)

    def preprocess_hashtags(self, tweet_string, repl):
        return Patterns.HASHTAG_PATTERN.sub(repl, tweet_string)

    def preprocess_mentions(self, tweet_string, repl):
        return Patterns.MENTION_PATTERN.sub(repl, tweet_string)

    def preprocess_reserved_words(self, tweet_string, repl):
        return Patterns.RESERVED_WORDS_PATTERN.sub(repl, tweet_string)

    def preprocess_emojis(self, tweet_string, repl):
        if not Defines.IS_PYTHON3:
            tweet_string = tweet_string.decode('utf-8')
        return Patterns.EMOJIS_PATTERN.sub(repl, tweet_string)

    def preprocess_smileys(self, tweet_string, repl):
        return Patterns.SMILEYS_PATTERN.sub(repl, tweet_string)

    def preprocess_numbers(self, tweet_string, repl):
        return re.sub(Patterns.NUMBERS_PATTERN, lambda m: m.groups()[0] + repl, tweet_string)

    def remove_unneccessary_characters(self, tweet_string):
        return ' '.join(tweet_string.split())

    def get_token_string_from_method_name(self, method_name):
        token_string = method_name.rstrip('s')
        token_string = token_string.split('_')[1]
        token_string = token_string.upper()
        token_string = '$' + token_string + '$'
        return token_string    
    
    
    
    
class Utils:

    def __init__(self):
        pass

    def get_worker_methods(self, object, prefix):
        all_methods = dir(object)
        relevant_methods = list(filter(lambda x: x.startswith(prefix), all_methods))

        # Filtering according to user's options
        prefixed_filtered_methods = [prefix+fm for fm in Defines.FILTERED_METHODS]
        filtered_methods = list(filter(lambda x: x in prefixed_filtered_methods, relevant_methods))

        # Prioritising
        offset = 0
        for ind, pri_method in enumerate(Defines.PRIORITISED_METHODS):
            prefixed_pri_method = prefix + pri_method
            if pri_method in filtered_methods:
                filtered_methods.remove(prefixed_pri_method)
                filtered_methods.insert(offset+ind, prefixed_pri_method)

        return filtered_methods    
    
    
class ParseResult:
    urls = None
    emojis = None
    smileys = None
    numbers = None
    hashtags = None
    mentions = None
    reserved_words = None

    def __init__(self):
        pass


class ParseItem:
    def __init__(self, start_index, end_index, match):
        self.start_index = start_index
        self.end_index = end_index
        self.match = match

    def __repr__(self):
        return '(%d:%d) => %s' % (self.start_index, self.end_index, self.match)


class Parse:

    def __init__(self):
        self.u = Utils()

    def parse(self, tweet_string):
        parse_result_obj = ParseResult()

        parser_methods = self.u.get_worker_methods(self, Defines.PARSE_METHODS_PREFIX)

        for a_parser_method in parser_methods:
            method_to_call = getattr(self, a_parser_method)
            attr = a_parser_method.split('_')[1]

            items = method_to_call(tweet_string)
            setattr(parse_result_obj, attr, items)

        return parse_result_obj

    def parser(self, pattern, string):

        match_items = []
        number_match_max_group_count = 2

        for match_object in re.finditer(pattern, string):
            start_index = match_object.start()
            end_index = match_object.end()

            if Patterns.NUMBERS_PATTERN == pattern and number_match_max_group_count == len(match_object.groups()):
                match_str = match_object.groups()[1]
            else:
                match_str = match_object.group()

            if not Defines.IS_PYTHON3:
                parse_item = ParseItem(start_index, end_index, match_str.encode('utf-8'))
            else:
                parse_item = ParseItem(start_index, end_index, match_str)

            match_items.append(parse_item)

        if len(match_items):
            return match_items

    def parse_urls(self, tweet_string):
        return self.parser(Patterns.URL_PATTERN, tweet_string)

    def parse_hashtags(self, tweet_string):
        return self.parser(Patterns.HASHTAG_PATTERN, tweet_string)

    def parse_mentions(self, tweet_string):
        return self.parser(Patterns.MENTION_PATTERN, tweet_string)

    def parse_reserved_words(self, tweet_string):
        return self.parser(Patterns.RESERVED_WORDS_PATTERN, tweet_string)

    def parse_emojis(self, tweet_string):
        if not Defines.IS_PYTHON3:
            tweet_string = tweet_string.decode('utf-8')
        return self.parser(Patterns.EMOJIS_PATTERN, tweet_string)

    def parse_smileys(self, tweet_string):
        return self.parser(Patterns.SMILEYS_PATTERN, tweet_string)

    def parse_numbers(self, tweet_string):
        return self.parser(Patterns.NUMBERS_PATTERN, tweet_string)
preprocessor = Preprocess()
parser = Parse()

def clean(tweet_string):
    
    cleaned_tweet_string = preprocessor.clean(tweet_string, Functions.CLEAN)
    return cleaned_tweet_string

def preprocess_imply(tweet_string):
    
    cleaned_tweet_string = preprocessor.imply_preprocess(tweet_string, Functions.IMPLY)
    return cleaned_tweet_string

def tokenize(tweet_string):
    
    tokenized_tweet_string = preprocessor.clean(tweet_string, Functions.TOKENIZE)
    return tokenized_tweet_string

def parse(tweet_string):

    parsed_tweet_obj = parser.parse(tweet_string)
    return parsed_tweet_obj

def set_options(*args):
    
    Defines.FILTERED_METHODS = list(args)


    

