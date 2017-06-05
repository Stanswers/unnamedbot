import os
from setuptools import setup

setup(
		name = 'unnamedbot',
		version = '0.0.1',
		author = 'Justin Helgesen',
		author_email = 'justinhelgesen@gmail.com',
		license = 'BSD',
		url = 'http://my.site.com',
		description = ('Simple Bot the polls twitter and posts to slack webhooks'),
		long_description='Kill All Humans',
		keywords = 'twitter-python, slack',
		classifiers=[
			'Development Status :: 3 - Alpha',
			'Topic :: Utilities',
			'License :: OSI Approved :: BSD License',
		],

		install_requires=['python-twitter', 'requests'],
		packages=['unnamedbot'],
		test_suite='test'
)
