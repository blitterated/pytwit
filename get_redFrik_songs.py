import sys
import datetime

import twitter
from twcred import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


class Twert:

    def __init__(self, tweet):
        self._username = tweet.user.screen_name

        self.created_at = tweet.created_at
        self.url = self._create_url_from_id(twid=tweet.id_str)
        self.text = tweet.full_text  # .text is empty when tweet_mode is "extended"

    def __str__(self):
        return "\n".join([self.created_at_formatted, self.url, self.text]) + "\n"

    def _create_url_from_id(self, twid):
        return "https://twitter.com/{u}/status/{twid}".format(u=self._username, twid=twid)

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, a_date):
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
        self._created_at = datetime.datetime.strptime(a_date, dt_fmt)

    @property
    def created_at_formatted(self):
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        # %b        month abbrev.
        # %d        day of month, zero padded
        # %Y        year with century

        dt_fmt = "%b %d, %Y"
        return self._created_at.strftime(dt_fmt)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text


def get_timeline(api=None, screen_name=None):
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


def filter_tweets(timeline=None, filter_term=""):
    return [tw for tw in timeline if filter_term in tw.full_text]


def output_twert_to_file(file=None, twert=None):
    file.write("// {} \n".format(twert.created_at_formatted))
    file.write("// {} \n".format(twert.url))
    file.write("// notes: \n")
    file.write("// audio rating: \n")
    file.write("// spectrograph rating: \n")
    file.write(twert.text)
    file.write("\n"*3)


def main():
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET,
                      tweet_mode="extended")

    screen_name = sys.argv[1]
    print(screen_name)
    timeline = get_timeline(api=api, screen_name=screen_name)

    sc_tweets = filter_tweets(timeline=timeline, filter_term="// #SuperCollider")
    print(len(sc_tweets))

    filename = '{sn}_tweets.txt'.format(sn=screen_name.replace("@", ""))

    with open(filename, 'w+') as f:
        for tweet in sc_tweets:
            output_twert_to_file(f, Twert(tweet))


if __name__ == "__main__":
    main()
