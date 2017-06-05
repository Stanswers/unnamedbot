#!/usr/bin/env python

import logging
import os
import sys

import unnamedbot

def main(argv):
	try:
		# TODO - Actually validate arguments and get logging parameters from commandline
		logging.basicConfig(format="%(asctime)s %(levelname)-7s %(module)-20s %(message)s", level=logging.DEBUG)
		listeners = []
		for webhook in argv[6::]:
			listeners.append(unnamedbot.SlackListener(webhook))
		logging.info('Starting Twitter Timeline Feed')
		feed = unnamedbot.TwitterTimelineFeed(argv[1], argv[2], argv[3], argv[4], argv[5], listeners)
		feed.run()
	except Exception as e:
		sys.stderr.write('%s\nUSAGE: %s\n' % (e, argv[0]))
		sys.stderr.flush()

if __name__ == '__main__':
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		print('')
