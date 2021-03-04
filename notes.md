### create the virtual env
```sh
pyenv virtualenv 3.7.0 pytwit
pyenv activate pytwit
pip install -U pip
```

### create an app
https://developer.twitter.com/en/apps
https://developer.twitter.com/en/apps/17847827
python-twitter-playground

### install deps
```sh
pip install python-twitter
```

### virtualenv enable
```sh
pyenv activate py
```

### connect to twitter
```python
import twitter
api = twitter.Api(consumer_key = "<YOUR_CONSUMER_KEY>",
                  consumer_secret = "<YOUR_CONSUMER_SECRET>",
                  access_token_key = "<YOUR_ACCESS_TOKEN_KEY>",
                  access_token_secret = "<YOUR_ACCESS_TOKEN_SECRET>")

api = twitter.Api(consumer_key = "<YOUR_CONSUMER_KEY>",
                  consumer_secret = "<YOUR_CONSUMER_SECRET>",
                  access_token_key = "<YOUR_ACCESS_TOKEN_KEY>",
                  access_token_secret = "<YOUR_ACCESS_TOKEN_SECRET>",
                  tweet_mode="extended")

timeline = api.GetUserTimeline(screen_name="@redFrik", count=1000)

len(timeline)
timeline[0]
dir(timeline[0])
timeline[0].created_at
timeline[0].text
timeline[0].tweet_mode
timeline[1].full_text

sc_tweets = [tw for tw in timeline if "// #SuperCollider" in tw.full_text]
len(sc_tweets)

from pprint import pprint
pprint(timeline)
pprint(timeline[0])

pprint(sc_tweets)
pprint(sc_tweets[0])
```

### Example json status returned by API

```json
{
  "created_at": "Sat Jan 30 14:32:27 +0000 2021",
  "id": 1355524280356892700,
  "id_str": "1355524280356892677",
  "text": "//play: left&amp;right arrow keys\nfork{p=19;x=0;do(inf,{|i|if(i%99==0,{postln('score: '++div(i,99))});t=cos(i/5)/5+cos(… https://t.co/OC4klizrJm",
  "truncated": true,
  "entities": {
    "hashtags": [],
    "symbols": [],
    "user_mentions": [],
    "urls": [
      {
        "url": "https://t.co/OC4klizrJm",
        "expanded_url": "https://twitter.com/i/web/status/1355524280356892677",
        "display_url": "twitter.com/i/web/status/1…",
        "indices": [
          121,
          144
        ]
      }
    ]
  },
  "source": "<a href=\"https://mobile.twitter.com\" rel=\"nofollow\">Twitter Web App</a>",
  "in_reply_to_status_id": null,
  "in_reply_to_status_id_str": null,
  "in_reply_to_user_id": null,
  "in_reply_to_user_id_str": null,
  "in_reply_to_screen_name": null,
  "user": {
    "id": 132238223,
    "id_str": "132238223",
    "name": "Fredrik Olofsson",
    "screen_name": "redFrik",
    "location": "",
    "description": "",
    "url": "http://t.co/hSMuCRhzCE",
    "entities": {
      "url": {
        "urls": [
          {
            "url": "http://t.co/hSMuCRhzCE",
            "expanded_url": "http://fredrikolofsson.com",
            "display_url": "fredrikolofsson.com",
            "indices": [
              0,
              22
            ]
          }
        ]
      },
      "description": {
        "urls": []
      }
    },
    "protected": false,
    "followers_count": 836,
    "friends_count": 0,
    "listed_count": 30,
    "created_at": "Mon Apr 12 17:39:21 +0000 2010",
    "favourites_count": 13,
    "utc_offset": null,
    "time_zone": null,
    "geo_enabled": false,
    "verified": false,
    "statuses_count": 586,
    "lang": null,
    "contributors_enabled": false,
    "is_translator": false,
    "is_translation_enabled": false,
    "profile_background_color": "C0DEED",
    "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
    "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
    "profile_background_tile": false,
    "profile_image_url": "http://pbs.twimg.com/profile_images/1045148567/block01-streck12_normal.gif",
    "profile_image_url_https": "https://pbs.twimg.com/profile_images/1045148567/block01-streck12_normal.gif",
    "profile_link_color": "1DA1F2",
    "profile_sidebar_border_color": "C0DEED",
    "profile_sidebar_fill_color": "DDEEF6",
    "profile_text_color": "333333",
    "profile_use_background_image": true,
    "has_extended_profile": false,
    "default_profile": true,
    "default_profile_image": false,
    "following": true,
    "follow_request_sent": false,
    "notifications": false,
    "translator_type": "none"
  },
  "geo": null,
  "coordinates": null,
  "place": null,
  "contributors": null,
  "is_quote_status": false,
  "retweet_count": 1,
  "favorite_count": 12,
  "favorited": true,
  "retweeted": false,
  "lang": "en"
}
```


### Example of formatted status

    // Aug 5, 2017
    // https://twitter.com/redFrik/status/893964744390037506
    // notes:  rhythmic chirping, Spectrograph
    // audio rating: *****
    // spectrograph rating: *****
    play{a=SinOsc;b=Duty;c={Dseq([5,1,3,2],1/0)};a.ar(b.ar(e=1/[8,4],0,c.()*b.ar(e/4,0,c.()))*b.ar(1/e,0,c.()*28.8))*a.ar(e/9)}


# References
* [python-twitter documentation](https://python-twitter.readthedocs.io/en/latest/)
* [Keyword (Named) Arguments in Python: How to Use Them](https://treyhunner.com/2018/04/keyword-arguments-in-python/)
* [Going From a List to a String in Python With .join()](https://realpython.com/python-string-split-concatenate-join/#going-from-a-list-to-a-string-in-python-with-join)
* [How to create a custom string representation for a class object? (Stack Overflow)](https://stackoverflow.com/a/4932466)
* [Python Classes and Objects](https://www.geeksforgeeks.org/python-classes-and-objects/)
* [Getting the class name of an instance? (Stack Overflow)](https://stackoverflow.com/a/511059)
* [Accessing Dictionary Values](https://realpython.com/python-dicts/#accessing-dictionary-values)
* [Built in Functions (dir)](https://docs.python.org/3/library/functions.html#dir)
* [Get first N items of list (Stack Overflow)](https://stackoverflow.com/a/41284450)
* [How to repeat a string in Python](https://www.kite.com/python/answers/how-to-repeat-a-string-in-python)
* [Converting Strings to datetime in Python](https://stackabuse.com/converting-strings-to-datetime-in-python/)
* [strftime() and strptime() Format Codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
* [Retreive tweet full text when tweet_mode is extended](https://github.com/tweepy/tweepy/issues/878)
* [Python @property decorator](https://www.programiz.com/python-programming/property)
* [Python: Check if String Contains Substring](https://stackabuse.com/python-check-if-string-contains-substring/)
* [if/else in a list comprehension](https://stackoverflow.com/a/4260304)
* [How To Pretty Print in Python](https://betterprogramming.pub/how-to-pretty-print-in-python-9b1d8764d151)
*




# Gripes

```
I hate this kind of bullshit. If you just “vanilla” request tweets from twitter, you get the tweet truncated to 140 chars and the tweet’s url (compatibility mode).
If you specify tweet_mode=“extended”, you get all the chars in the tweet, but zero urls.
So much for element of least surprise
```

