#!/usr/bin/env python

import json
import logging
import requests

class SlackListener():
    webhook = None

    def __init__(self, webhook):
        self.webhook = webhook

    def post(data, headers):
        requests.post(self.webhook, data=data, headers=headers)

    def recieve(self, message):
        data = json.dumps({'text':message})
        headers = {'Content-Type':'application/json', 'Content-Length':str(len(data))}
        logging.debug('post message to webhook: %s', self.webhook)
        self.post(data, headers)

