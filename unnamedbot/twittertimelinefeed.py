#!/usr/bin/env python

import logging
import sched
import time
import twitter

class TwitterTimelineFeed():
    last_tweet_id = None
    twitter_client = None
    user_name = None
    listeners = None

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret, user_name, listeners):
        self.twitter_client = twitter.Api(consumer_key, consumer_secret,
                access_token_key, access_token_secret, 'utf-8', timeout=1)
        self.user_name = user_name
        self.listeners = listeners

    def poll_twitter(self):
        try:
            tweets = self.get_tweets(self.user_name, self.last_tweet_id, None if self.last_tweet_id else 1)
            logging.debug('poll %s twitter feed, found %s tweets', self.user_name, len(tweets))
            if len(tweets) <= 0:
                return
            logging.debug('update last trump id [%s->%s]', self.last_tweet_id, tweets[0].id)
            # Don't broadcast first tweet to avoid sending duplicates after restart
            if not self.last_tweet_id:
                self.last_tweet_id = tweets[0].id
                return
            self.last_tweet_id = tweets[0].id
            # The newest tweet is first in the list, handle the oldest tweet first
            for tweet in reversed(tweets):
                try:
                    logging.info('broadcast new tweet [%s]: %s', tweet.id, tweet.text)
                    self.broadcast(tweet.text)
                except Exception as e:
                    logging.exception('failed process tweet')
        except Exception as e:
            logging.exception('failed to poll %s twitter feed', self.user_name, e)

    def get_tweets(self, screen_name, since_id, count):
        return self.twitter_client.GetUserTimeline(screen_name=screen_name,
                since_id=since_id, count=count)

    def broadcast(self, message):
        for listener in self.listeners:
            listener.recieve(message)

    def periodic_action(self, scheduler, interval, action, actionargs=()):
        scheduler.enter(interval, 1, self.periodic_action, (scheduler, interval, action, actionargs))
        action(*actionargs)

    def run(self):
        logging.debug('server forever')
        s = sched.scheduler(time.time, time.sleep)
        s.enter(1, 1, self.periodic_action, (s, 60, self.poll_twitter, ()))
        s.run()
