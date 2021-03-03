import sys
import datetime

import twitter
from twcred import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

class Twert:
    def __init__(self, tweet):
        self.created_at = self.parse_date(tweet.created_at)
        #self.url = tweet.urls[0].expanded_url
        self.text = tweet.full_text  # .text is empty when tweet_mode is "extended"

    def __str__(self):
       # return "\n".join([self.created_at, self.url, self.text]) + "\n"
        return "\n".join([self.fmt_created_at(), self.text]) + "\n"

    def parse_date(self, a_date):
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        # %a        weekday abbrev.
        # %b        month abbrev.
        # %d        day of month, zero padded
        # %H        hour, 24 hour clock
        # %M        minute, zero padded
        # %S        seconds, zero padded
        # %z        UTC offset
        # %Y        year with century

        dt_fmt = "%a %b %d %H:%M:%S %z %Y"
        return datetime.datetime.strptime(a_date, dt_fmt)

    def fmt_created_at(self):
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        # %b        month abbrev.
        # %d        day of month, zero padded
        # %Y        year with century

        dt_fmt = "%b %d, %Y"
        return self.created_at.strftime(dt_fmt)


def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=1000)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


def main():
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET,
                      tweet_mode="extended")

    screen_name = sys.argv[1]
    print(screen_name)
    timeline = get_tweets(api=api, screen_name=screen_name)

    with open('redFrik_SC_tweets.txt', 'w+') as f:
        for tweet in timeline[:20]:
            f.write("-"*20)
            f.write(str(Twert(tweet)))
            #print(type(tweet.created_at).__name__)


if __name__ == "__main__":
    main()
