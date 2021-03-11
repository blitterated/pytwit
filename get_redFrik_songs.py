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


class TwertTimeline:

    def __init__(self, screen_name=None, timeline=None):
        """Constructor

        :return: A new TwitterClient instance
        """
        self.screen_name = screen_name
        self.timeline = timeline

    def __len__(self):
        return len(self.timeline)

    def __iter__(self):
        return iter(self.timeline)

    @property
    def screen_name(self):
        """Get a given user's screen_name

        :return: a screen_name
        """
        return self._screen_name

    @screen_name.setter
    def screen_name(self, screen_name):
        """Set a given user's screen_name

        :param screen_name: a given user's screen_name
        """
        self._screen_name = screen_name

    @property
    def timeline(self):
        """Get a given user's timeline of statuses

        :return: a python-twitter Timeline object
        """
        return self._timeline

    @timeline.setter
    def timeline(self, timeline):
        """Set a given user's timeline of statuses

        :param timeline: a given user's timeline pulled from Twitter's API. A python-twitter timeline object.
        """
        self._timeline = timeline

    def filter(self, filter_term=""):
        """Filter through statuses in the timeline that match the filter_term

        :param filter_term: A discrete text string used for matching
        :return: a new, filtered TwertTimeline
        """
        filtered_timeline = [s for s in self.timeline if filter_term in s.full_text]
        return TwertTimeline(self.screen_name, filtered_timeline)


class TwitterClient:

    def __init__(self, twitter_api=None):
        """Constructor

        :return: A new TwitterClient instance
        """
        self._api = twitter_api

    def get_timeline(self, screen_name=None):
        """Fetch the entirety of statuses from a user's (screen_name's) timeline

        This pages through and pulls down statuses in batches since Twitter only allows us to pull a certain number
        per call

        :param screen_name: The user's screen name on Twitter, e.g. "@foobar"
        :return: a python-twitter Timeline object
        """
        timeline = self._api.GetUserTimeline(screen_name=screen_name, count=1000)
        earliest_tweet = min(timeline, key=lambda x: x.id).id
        print("getting tweets before:", earliest_tweet)

        while True:
            tweets = self._api.GetUserTimeline(
                screen_name=screen_name, max_id=earliest_tweet, count=200
            )
            new_earliest = min(tweets, key=lambda x: x.id).id

            if not tweets or new_earliest == earliest_tweet:
                break
            else:
                earliest_tweet = new_earliest
                print("getting tweets before:", earliest_tweet)
                timeline += tweets

        return TwertTimeline(screen_name, timeline)


def output_twert_to_file(file=None, twert=None):
    file.write("// {} \n".format(twert.created_at_formatted))
    file.write("// {} \n".format(twert.url))
    file.write("// notes: \n")
    file.write("// audio rating: \n")
    file.write("// spectrograph rating: \n")
    file.write(twert.text)
    file.write("\n" * 3)


def main():
    screen_name = sys.argv[1]
    print(screen_name)

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET,
                      tweet_mode="extended")

    client = TwitterClient(twitter_api=api)
    timeline = client.get_timeline(screen_name=screen_name) \
        .filter(filter_term="// #SuperCollider")
    print(len(timeline))

    filename = '{sn}_tweets.txt'.format(sn=screen_name.replace("@", ""))

    with open(filename, 'w+') as f:
        for tweet in timeline:
            output_twert_to_file(f, Twert(tweet))


if __name__ == "__main__":
    main()
