# built by following
# http://blog.mollywhite.net/twitter-bots-pt2/
#
# link to bot
# https://twitter.com/ConUHackYP
#
# Natural language
# http://www.nltk.org/

# find and reply to tweets
# http://www.dototot.com/reply-tweets-python-tweepy-twitter-bot/
#
# tweepy doc (search)
# http://docs.tweepy.org/en/latest/api.html#API.search
#
# yellow pages API
# http://api.sandbox.yellowapi.com/FindBusiness/?what=florists&where=Vancouver&UID=127.0.0.1&apikey=g8vnmwnr74bzc2wftk3emaxh&fmt=JSON
#
#
#
#
#
#
#

# tweet keys
#'place', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'truncated', 'created_at', 'metadata', 'entities', 'in_reply_to_screen_name', 'lang', 'id', 'retweeted', 'in_reply_to_user_id_str', 'is_quote_status', 'contributors', 'retweet_count', 'author', 'geo', 'favorite_count', 'in_reply_to_user_id', 'source', 'text', 'coordinates', '_api', 'favorited', 'source_url', '_json', 'id_str', 'user'])

import nltk
import tweepy
from secrets import *
import urllib.request
import json
import codecs
import threading

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

#
# words that will not be added to the API search
#
block_words = ["@", "rt", "hey", "-", "askyp", ""]

#
# global holder for tweets, and seen ids
#
twts = []

f = open("cache.txt", "r")
seen_id = f.read().split(",")
f.close()

#
# when called, takes first tweet in search
# make call to yellow pages
# issues a response tweet to person
#
def respondToTweet():
    global twts # get variable from global scope
    global seen_id

    # refresh tweet list if necessary
    if(len(twts) == 0):

        #
        # get tweets with search term
        #
        twts = api.search(q="askYP")

    #
    # pop most recent tweet
    #
    s = twts[0]
    twts = twts[1:]

    if(not str(s.id) in seen_id):
        seen_id.append(str(s.id))

        #
        # write seen ids to file
        #
        f = open("cache.txt", "w")
        f.write( ",".join(seen_id) )
        f.close()


        # add username to block_words
        block_words.append(s.user.screen_name.lower())

        print("tweet: " + s.text)
        print("")

        #
        # figure out tags for words in tweet "s"
        #
        tokens = nltk.word_tokenize( s.text )
        tagged = nltk.pos_tag(tokens)

        #
        # build array of NNP terms
        #
        terms = []
        for t in tagged:
            if(t[1] in ["NNP", "NNS", "JJ", "NN"]):
                if(not t[0].lower() in block_words):
                    terms.append( t[0].lower() )

        #
        # build list of search terms
        #
        terms_string = ""
        if( len(terms) == 1 ):
            terms_string = terms[0]

        # add username to block_words
        block_words.append(s.user.screen_name.lower())

        print("tweet: " + s.text)
        print("")

        #
        # figure out tags for words in tweet "s"
        #
        tokens = nltk.word_tokenize( s.text )
        tagged = nltk.pos_tag(tokens)

        #
        # build array of NNP terms
        #
        terms = []
        for t in tagged:
            if(t[1] in ["NNP", "NNS", "JJ", "NN"]):
                if(not t[0].lower() in block_words):
                    terms.append( t[0].lower() )

        #
        # build list of search terms
        #
        terms_string = ""
        if( len(terms) == 1 ):
            terms_string = terms[0]

        elif( len(terms) > 1 ):
            terms_string = ", ".join(terms[:-1]) + ", and " + terms[-1]

        #
        # a string of terms that can be encoded into the yellow pages url
        #
        url_terms = terms_string.replace(" ", "%20")

        #
        # make request to yellow pages.
        #
        yellow_url = "http://api.sandbox.yellowapi.com/FindBusiness/?what="+ url_terms +"&where=Montreal&UID=127.0.0.1&apikey=XXXXXX&fmt=JSON"

        if(not url_terms == ""):

            print("*** will query")
            print(yellow_url)
            print("")

            res = ""
            try:
                with urllib.request.urlopen(yellow_url) as response:
                    reader = codecs.getreader("utf-8")
                    res = json.load(reader(response))

            except:
                threading.Timer(6, respondToTweet).start()
                return 0
            
            #
            # trim listings to max of 2
            #
            if( len(res["listings"]) > 2):
                res["listings"] = res["listings"][-2:]

            #
            # create string from listings found
            #
            places_array = []
            for place in res["listings"]:
                places_array.append(place["name"] + " at " + place["address"]["street"])
            places_string = " OR ".join(places_array)

            #
            # must have parsed at least one search term
            if( not terms_string == "" ):

                # if nothing else reccomend yellowpages
                if(places_string == ""):
                    places_string = "yellowpages.ca"

                #
                # send reply message to user
                #
                message = "@" + s.user.screen_name
 
                limitMessage = message + " to find " + terms_string + " check out: " + places_string
                limitMessage = limitMessage[0:139]
                api.update_status(limitMessage, s.id)

                #api.update_status(message + " to find " + terms_string + " check out: " + places_string, s.id)
 

                # debug
                debug_message = message + " to find " + terms_string + " check out: " + places_string
                print("*** *** *** *** *** *** ***")
                print(debug_message)
                print("*** *** *** *** *** *** ***")

                print("")

        else:
            print("... no products found in tweet")
            print("")
            threading.Timer(1.5, respondToTweet).start()
            return 0

        threading.Timer(8.0, respondToTweet).start()

    else: # id has been seen
        print("searching...")
        threading.Timer(1.5, respondToTweet).start()



#
# initial call to respondToTweet then it's called every n sec
#
respondToTweet()





#end
