
# coding: utf-8

# In[396]:

# Loading all the required libraries

#import nltk
import string
#nltk.download()
import re
import logging
from gensim import corpora, models, similarities
import pandas
from pandas import DataFrame
from gensim import corpora, models, similarities
import time


# In[323]:

# Loading required data
# xl_mon - "they"
# xl_tkl - "we"

xl_mon = pandas.ExcelFile(u'')
xl_tkl = pandas.ExcelFile(u'')
df_tkl = xl_tkl.parse(0)
df_mon = xl_mon.parse(0)


# In[404]:

def punc_delete(todelete):
    
    """
    Function delete unnecessary punctuation, spaces and lower case of the string.
    Also delete stop(unnecessary) words
    Works with list of strings.
    """
    
    f_list = []
    for x in todelete:
        #print re.sub("[\.\t\,\:;\(\)\.\-\*\%\/]", "", x.lower(), 0, 0)
        stoplist = set(u'ассортиментe|ассортимент|ассорт| в | мл | кг | г | л '.split("|"))
        temp = x.lower()
        for i in stoplist:
            temp = re.sub(i, "", temp, 0, 0)
        f_list.append(re.sub("[\.\t\,\:;\.\-\*\%\/\'\`\’ ]", "", temp, 0, 0))    
    return f_list


# In[255]:

# Convert dataframes to lists
# Delete punctuation in "our" list

mon_list = df_mon[0].tolist()
tkl_list = df_tkl.ix[:,10].tolist()
f_list = punc_delete(tkl_list)

# for x in f_list[:30]:
#     print x


# In[240]:

def ngram_gen(string, n):
    
    """
    Function generates N-gramms (N-length sequences of letters) from origin string.
    Returns list of strings.
    """    
    
    ngram = [string[i:i+n] for i in range(len(string)-n+1) if string[i:i+n] != " " * n]
    return ngram


# In[241]:

def ngram_text(f_list, n):
    
    """
    Function generates N-gramms (N-length sequences of letters) from test (list of strings).
    Returns list of lists of strings.
    """
    
    ngram_list = []
    for x in f_list:
        l = ngram_gen(x.lower(), n)
        ngram_list.append(l)
    #return DataFrame(ngram_list)
    return ngram_list


# In[256]:

# Generating 3-gramms from "our" tkl

ngrams = ngram_text(f_list, 3)


# In[266]:

# Creating dictionary of ngrams (tokens)

dictionary = corpora.Dictionary(ngrams)
print dictionary


# In[263]:

# Creating corpus from ngrams
# The function doc2bow() simply counts the number of occurences of each distinct word, 
# converts the word to its integer word id and returns the result as a sparse vector. 
# The sparse vector [(0, 1), (1, 1)] therefore reads: in the document 
# “Human computer interaction”, the words computer (id 0) and human (id 1) appear once; 
# the other ten dictionary words appear (implicitly) zero times.

corpus = [dictionary.doc2bow(text) for text in ngrams]


# In[267]:

# Defining a 2000-dimensional LSI space with a corpus

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2000)


# In[269]:

# Transform corpus to defined 2000-dimensional LSI space and index it

index = similarities.MatrixSimilarity(lsi[corpus]) 


# In[410]:

# Generating list of "theirs" tkl.

new_doc = list(set(mon_list))#
for x in punc_delete(new_doc):
    print x
new_tok = ngram_text(punc_delete(new_doc), 3)
#for x in new_tok:
#    print x
new_vec = []
for x in new_tok:
    new_vec.append(dictionary.doc2bow(x))
# new_vec = dictionary.doc2bow(new_tok)
# for x in new_tok:
#     print x
# for x in new_vec:
#    print new_vec


# In[407]:

vec_lsi = []
for x in new_vec:
    vec_lsi.append(lsi[x])


# In[408]:

numbers = []

for x in vec_lsi:
    sims = index[x]
    #print sims[:2]
    sims = sorted(enumerate(sims), key = lambda item: -item[1])
    print sims[0:3]
    numbers.append(map(lambda (x,y):x, sims[0:5]))
    #print numbers


# In[411]:

final_list = []
for x, val in enumerate(numbers):
    semifinal_list = []
    #print x
    semifinal_list.append(new_doc[x])
    print x , "",new_doc[x], ": "
    #print numbers
    for xx in numbers[x]:
        print "         " + df_tkl.ix[xx,10] # + "    " + str(df_tkl.ix[x, 0])
        semifinal_list.append(df_tkl.ix[xx,10])
    print ""
    final_list.append(semifinal_list)


# In[412]:

df_all = DataFrame(final_list)
adress = u'' + str(time.strftime("%Y-%m-%d")) + '_comparator.xlsx'
print adress
writer = pandas.ExcelWriter(adress) #, engine='xlsxwriter')
df_all.to_excel(writer, sheet_name = "Final")
writer.save()

