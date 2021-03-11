import sys
import datetime

import twitter
from twcred import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


class Twert:
    """A representation of an individual Twitter status"""

    def __init__(self, tweet):
        """Constructor

        :return: A new Twert instance
        """
        self._username = tweet.user.screen_name

        self.created_at = tweet.created_at
        self.url = self._create_url_from_id(twid=tweet.id_str)
        self.text = tweet.full_text  # .text is empty when tweet_mode is "extended"

    def __str__(self):
        r"""Override of standard __str__ method

        Use this in methods that will treat a Twert as a string, e.g. logging methods.

        :return: A \n separated string of the interesting fields from the status
        """
        return "\n".join([self.created_at_formatted, self.url, self.text]) + "\n"

    def _create_url_from_id(self, twid):
        """ Create a URL from the status id

        :param twid: The id of a Twitter status. Found in the json fields "id" or "id_str"
        :return: A URL in string format
        """
        return "https://twitter.com/{u}/status/{twid}".format(u=self._username, twid=twid)

    @property
    def created_at(self):
        """Date & time when the status was posted

        :return: Datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, a_date):
        """Sets the datetime of when a status was created

        The created_at date in the json has the following format:

            Sat Jan 30 14:32:27 +0000 2021

        It's parsed using the following codes in the formatting string taken from the docs.
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        %a        weekday abbrev.
        %b        month abbrev.
        %d        day of month, zero padded
        %H        hour, 24 hour clock
        %M        minute, zero padded
        %S        seconds, zero padded
        %z        UTC offset
        %Y        year with century

        :param a_date: The string representation of the status' creation date and time. It comes from the "created_at" field in the status' json
        """
        dt_fmt = "%a %b %d %H:%M:%S %z %Y"
        self._created_at = datetime.datetime.strptime(a_date, dt_fmt)

    @property
    def created_at_formatted(self):
        """The created_at date formatted for printing

        The date & time are formatted using the following codes the docs.
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        %b        month abbrev.
        %d        day of month, zero padded
        %Y        year with century

        :return: Formatted created_at string
        """
        dt_fmt = "%b %d, %Y"
        return self._created_at.strftime(dt_fmt)

    @property
    def url(self):
        """URL of the status on Twitter

        :return: URL string
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets URL of the status on Twitter

        :param url: URL string
        """
        self._url = url

    @property
    def text(self):
        """The body text of the status on Twitter

        :return: URL string
        """
        return self._text

    @text.setter
    def text(self, text):
        """Sets body text of the status

        :param text: Text found in the "text" json field of a Twitter status
        """
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
