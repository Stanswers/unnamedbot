#!/usr/bin/env python

import unittest

if __name__ == '__main__':
	runner = unittest.TextTestRunner()
	test_loader = unittest.TestLoader()
	test_suite = test_loader.discover('.', pattern='test_*.py')
	runner.run(test_suite)
