#!/usr/bin/env python3
"""
Created on Sat Oct 20 00:08:56 2018

@author: Vijaya Krishna (vgopala)
"""
"""
Design Decisions : 
    1) Converted all the words in the text to lower case.
    2) Removed the english language stop words.
    3) Removed the punctuations
    4) If the word is not in the given bag, a small probability of 1/(10**5) is assumed for P(word|location)  rather than zero.

"""
from collections import Counter
import timeit as t
import string
import sys

cities = ['San_Diego,_CA', 'San_Francisco,_CA', 'Manhattan,_NY', 'Los_Angeles,_CA', 'Houston,_TX', 'Chicago,_IL', 'Philadelphia,_PA', 'Toronto,_Ontario', 'Atlanta,_GA', 'Boston,_MA', 'Orlando,_FL', 'Washington,_DC']
# The words in this list taken from https://gist.github.com/sebleier/554280
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", \
             "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", \
             'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', \
             'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', \
             'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', \
             'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', \
             'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', \
             'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', \
             'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', \
             's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', \
             "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', \
             "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', \
             "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

#This function reads a text file and returns a list -- that has individual tweets as its elements, a dictionary -- that has
#all the 12 cities as key and list of tweets from that city as values, a integer -- that has the total tweets from the 12 cities.
def read_data(filename):
    city_tweets = {city : [] for city in cities}
    city_data = []
    total = 0
    with open(filename, 'r') as file:
        for line in file:
            city_data.append(line)
            tweet = line.split(" ", 1)
            if tweet[0] in cities:
                total += 1
                city_tweets[tweet[0]].append(tweet[1].lower())
    return city_data, city_tweets, total

#This function removes punctuation in the entries of a list of words
def remove_punctuation(lst):
    #The code taken from stack overflow begins
    #https://stackoverflow.com/questions/4371231/removing-punctuation-from-python-list-items
    lst = [''.join(c for c in s if c not in string.punctuation) for s in lst]
    #The code taken from stack overflow ends
    lst = [s for s in lst if s != '']
    return lst

#This function returns a dictionary of dictionaries that has probability of each word in each city.
def bag_of_words(tweet_dict):
    tweet_prob_bag = {city : {} for city in cities}
    for k in tweet_dict.keys():
        temp = ' '.join(tweet_dict[k])
        word_list = [word for word in remove_punctuation(temp.split()) if word not in stopwords]
        length = len(word_list)
        word_count = Counter(word_list)
        tweet_prob_bag[k] = {w : word_count[w]/float(length) for w in word_count}
    return tweet_prob_bag

#This function tests the working of the model in the testing dataset. It returns a list -- that has the estimated label and the actual label and the tweet, 
# a float -- that has the test set accuracy
def test_model(tweet_dict):
    output_list = []
    accuracy = 0
    for k in tweet_dict.keys():
        for line in tweet_dict[k]:
            city_pdict = {}
            for city in cities:
                prob = 1
                for word in remove_punctuation(line.split()):
                    if word not in stopwords:
                        p = bag[city][word] if word in bag[city].keys() else 1/float(10**5)
                        prob *= p
                city_pdict[city] = prob * number_tweets[city] / float(train_len)
            city_pdict = Counter(city_pdict)
            est_city = city_pdict.most_common()[0][0]
            output_list.append(est_city + " " + k + " " + line)
            if est_city == k:
                accuracy += 1
    
    accuracy = accuracy / float(test_len)
    return output_list, accuracy
 
#This function write the given list into a text file.   
def write_file(output_list, output_file):
    with open(output_file, 'w') as file:
        for l in output_list:
            file.write(l)

t1 = t.default_timer()

train_data, train_city_dict, train_len = read_data(sys.argv[1])

test_data, test_city_dict, test_len = read_data(sys.argv[2])

number_tweets = dict({ k : len(train_city_dict[k]) for k in train_city_dict })

bag = bag_of_words(train_city_dict)

output_list, accuracy = test_model(test_city_dict)

write_file(output_list, sys.argv[3])

print("Test Set Accuracy :", accuracy)

for city in bag.keys():
   print(city, [w for w, p in Counter(bag[city]).most_common(5)])
           
t2 = t.default_timer()
print("Time Taken %f seconds" % (round(t2-t1, 4)))