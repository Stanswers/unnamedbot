#!/usr/bin/env python

import sys
import unittest
import unnamedbot

from mock import Mock, call, patch, ANY

class TestTwitterTimelineFeed(unittest.TestCase):

	@patch('unnamedbot.TwitterTimelineFeed.get_tweets')
	def test_poll_twitter(self, mock_get_tweets):
		tweet0 = Mock()
		tweet0.id = 12345
		tweet0.text = 'HelloWorld'
		tweet1 = Mock()
		tweet1.id = 12346
		tweet1.text = 'HelloWorld!!'
		tweet2 = Mock()
		tweet2.id = 12347
		tweet2.text = 'helloworld'
		tweet3 = Mock()
		tweet3.id = 12348
		tweet3.text = 'foo'
		tweet4 = Mock()
		tweet4.id = 12349
		tweet4.text = 'bar'
		listeners = [ Mock(), Mock() ]
		server = unnamedbot.TwitterTimelineFeed('consumer_key',
				'consumer_secret',
				'access_token_key',
				'access_token_secret', 'realDonaldTrump', listeners)

		mock_get_tweets.return_value=[tweet0]

		server.poll_twitter()

		self.assertEqual(tweet0.id, server.last_tweet_id)
		mock_get_tweets.assert_called_once_with('realDonaldTrump', None, 1)
		for listener in listeners:
			listener.assert_not_called()

		mock_get_tweets.return_value=[tweet2,tweet1]

		server.poll_twitter()

		self.assertEqual(tweet2.id, server.last_tweet_id)
		mock_get_tweets.assert_called_with('realDonaldTrump', tweet0.id, None)
		self.assertEqual(2, mock_get_tweets.call_count)
		for listener in listeners:
			listener.assert_has_calls([call.recieve(tweet1.text), call.recieve(tweet2.text)])
			self.assertEqual(2, listener.recieve.call_count)

		mock_get_tweets.return_value=[tweet4,tweet3]

		server.poll_twitter()

		self.assertEqual(tweet4.id, server.last_tweet_id)
		mock_get_tweets.assert_called_with('realDonaldTrump', tweet2.id, None)
		self.assertEqual(3, mock_get_tweets.call_count)
		for listener in listeners:
			listener.assert_has_calls([call.recieve(tweet1.text), call.recieve(tweet2.text), call.recieve(tweet3.text), call.recieve(tweet4.text)])
			self.assertEqual(4, listener.recieve.call_count)

if __name__ == '__main__':
	unittest.main()

