import sys
import datetime
import importlib

import twitter

class Twert:
    """A representation of an individual Twitter status"""

    def __init__(self, tweet):
        """Constructor

        :return: A new Twert instance
        """
        self._screen_name = tweet.user.screen_name

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
        return "https://twitter.com/{u}/status/{twid}".format(u=self._screen_name, twid=twid)

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

        Converts python-twitter timeline of statuses into Twerts

        :return: A new TwertTimeline instance
        """
        if timeline is None:
            timeline = []
        self.screen_name = screen_name
        self.timeline = map(lambda t: Twert(t), timeline)

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
        filtered_timeline = [s for s in self.timeline if filter_term in s.text]
        new_timeline = TwertTimeline(self._screen_name, None)
        new_timeline.timeline = filtered_timeline
        return new_timeline


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

        Taken from the python-twitter examples here:

            https://github.com/bear/python-twitter/blob/master/examples/get_all_user_tweets.py#L23

        :param screen_name: The user's screen name on Twitter, e.g. "@foobar"
        :return: a TwertTimeline
        """
        timeline = self._api.GetUserTimeline(screen_name=screen_name, count=1000)
        earliest_tweet = min(timeline, key=lambda x: x.id).id

        while True:
            tweets = self._api.GetUserTimeline(
                screen_name=screen_name, max_id=earliest_tweet, count=200
            )
            new_earliest = min(tweets, key=lambda x: x.id).id

            if not tweets or new_earliest == earliest_tweet:
                break
            else:
                earliest_tweet = new_earliest
                timeline += tweets

        return TwertTimeline(screen_name, timeline)


class TwertTimelineFileWriter:

    def __init__(self, timeline):
        """ Constructor

        :param timeline: A python-twitter timeline
        """
        self._timeline = timeline
        self._filename = \
            '{sn}_tweets.txt'.format(sn=timeline.screen_name.replace("@", ""))

    def write(self):
        """Write statuses out to a file
        """
        with open(self._filename, 'w+') as f:
            for twert in self._timeline:
                f.write("// {} \n".format(twert.created_at_formatted))
                f.write("// {} \n".format(twert.url))
                f.write("// notes: \n")
                f.write("// audio rating: \n")
                f.write("// spectrograph rating: \n")
                f.write(twert.text)
                f.write("\n" * 3)


def main():
    secrets_file = sys.argv[2]
    print("Importing secrets from {}.".format(secrets_file))
    secrets = importlib.import_module(secrets_file)

    screen_name = sys.argv[1]
    print("Pulling tweets for {}.".format(screen_name))

    api = twitter.Api(consumer_key=secrets.CONSUMER_KEY,
                      consumer_secret=secrets.CONSUMER_SECRET,
                      access_token_key=secrets.ACCESS_TOKEN_KEY,
                      access_token_secret=secrets.ACCESS_TOKEN_SECRET,
                      tweet_mode="extended")

    client = TwitterClient(twitter_api=api)

    # TODO: the SuperCollider filtering is verrrry specific to one case. Push into another script or class.
    timeline = client.get_timeline(screen_name=screen_name) \
        .filter(filter_term="// #SuperCollider")

    TwertTimelineFileWriter(timeline).write()

    print("{} tweets processed.".format(len(timeline)))


if __name__ == "__main__":
    main()
