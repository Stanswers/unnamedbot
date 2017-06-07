#!/usr/bin/env python

import sys
import unittest

from unnamedbot import SlackListener
from mock import patch

class TestSlackListener(unittest.TestCase):

    @patch('requests.post')
    def test_recieve(self, mock_post):
        listener = SlackListener('https://webhook.com')
        message = 'This is a tweet'
        listener.recieve(message)
        mock_post.assert_called_once()


if __name__ == '__main__':
    unittest.main()
