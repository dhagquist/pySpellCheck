# Custom spell checker for parsing and processing tweet text
# Does not check for grammar and does not analyze context
# See bottom of file for issues and to-do's

import string
import time

# Loads English dictionary from file and loads into a list
# Returns dictionary as a list
def loaddict():
    dictionary = []
    numlines = sum(1 for line in open('dictionary.txt'))
    with open ("dictionary.txt", "r") as f:
        for i in range(numlines):
            dictionary.append(f.readline().replace('\n', ''))
    return dictionary

# Loads contractions from file and loads into a list
# Returns contractions as a list
def loadcontractions():
    contractions = []
    numlines = sum(1 for line in open('contractions.txt'))
    with open ("contractions.txt", "r") as f:
        for i in range(numlines):
            contractions.append(f.readline().replace('\n', ''))
    return contractions

# Takes a string of text, checks contractions, removes punctuation, hashtags, @'s, and URLS
# Returns the word/s of the text as a list
def processtext(text):
    text = text.lower()
    words = text.split()
    templist = []
    for word in words:
        word = word.strip()
        if word[0] != "#" and "http" not in word and "@" not in word:
            # Check for valid contraction, if valid, skip
            if word in contractions:
                templist.append(word)
                continue
            # Check for possessive nouns
            elif word[-2:] == "'s":
                word = word[:-2]
            punc = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
            word = word.translate(punc)
            word = word.strip()
            if " " in word:
                temp = word.split()
                templist.extend(temp)
            else:
                templist.append(word)
    words = templist
    return words

# Takes a string and checks each word against the dictionary
# Returns count of misspelled words as an integer and list of misspelled words
def spellcheck(text):
    words = processtext(text)
    count = 0
    misspelled = []
    for word in words:
        if word.isdigit():
            continue
        elif word not in dictionary:
            misspelled.append(word)
            count += 1
    return count, misspelled, words

# Test
t0 = time.time()
u0 = time.time()
# Only want to load these files once
global dictionary
dictionary = loaddict()
global contractions
contractions = loadcontractions()
u1 = time.time()

tweet1 = "Tihs is a tset. #hashtag http://test.com Look.There.asdf 2123098"
tweet2 = "Thid is test 2! #test2rules isn't they're pool's Carl's"
tweet3 = ""
tweet4 = '   ### !@# !hello123! "" can"t poo!p      '
tweets = [tweet1, tweet2, tweet3, tweet4]

r0 = time.time()
for tweet in tweets:
    q0 = time.time()
    count, misspelled, words = spellcheck(tweet)
    q1 = time.time()
    print "Time to process: " + str(q1 - q0)
    print "Text: " + str(tweet)
    print "Parsed words: " + str(words)
    print "Misspelled words: " + str(misspelled)
    print "Number of misspelled words: " + str(count) + "\n"
t1 = time.time()
total = t1-t0

print "Time to load dict/cont files: " + str(u1 - u0)
print "Time to run all tweets: " + str(t1 - r0)
print "Total time: " + str(total)

'''
Issues / To-Do's:

- If it's a word not in the dictionary and starts with a capital letter, it's
  probably a proper noun or name, or the beginning of a sentence.

- Account for internet slang e.g. lol, smdh, lmao

- 'they"re' --> 'they', 're'
   Yields inaccurate result since "they" and "re" are both words.
   Negligable? Possible non-issue with a large sample of tweets.
   
- Load dictionary into database and use SQL to search for words instead of list?

'''
