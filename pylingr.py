#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import simplejson
import urllib
import urllib2
import logging


class Lingr(object):
    __URL_BASE__ = 'http://lingr.com/api/'

    def __init__(self, user, password, apikey=""):
        self.user = user
        self.password = password
        self.apikey = apikey
        self.counter = 0

    def create_session(self):
        data = self.post('session/create', {
            'user': self.user,
            'password': self.password,
            'api_key': self.apikey,
            })
        if data:
            self.session = data['session']
            self.nickname = data['nickname']
        return data

    def get_rooms(self):
        data = self.get("user/get_rooms", {
            'session': self.session
            })
        if data:
            self.rooms = data['rooms']
        return data

    def subscribe(self, room=None, reset='true'):
        if not room:
            room = ','.join(self.rooms)
        data = self.post("room/subscribe", {
            'session': self.session,
            'room': room,
            'reset': reset
            })
        if data:
            self.counter = data['counter']
        return data

    def observe(self):
        data = self.get("event/observe", {
            'session': self.session,
            'counter': self.counter
            })
        if 'counter' in data:
            self.counter = data['counter']
        return data

    def say(self, room, text):
        data = self.post('room/say', {
            'session': self.session,
            'room': jroom,
            'nickname': self.nickname,
            'text': text})
        return data

    def post(self, path, params):
        r = self.get_opener().open(self.get_url(path),
                                     urllib.urlencode(params))
        return self.loads(r.read())

    def get(self, path, params):
        r = self.get_opener().open(self.get_url(path) + '?' +
            urllib.urlencode(params))
        return self.loads(r.read())

    def loads(self, json):
        data = simplejson.loads(json)
        if data['status'] == 'ok':
            return data
        else:
            print 'error'
            print data
        return None

    def get_url(self, path):
        url = self.__URL_BASE__
        if path == 'event/observe':
            url = self.__URL_BASE__
        return url + path

    def get_opener(self):
        opener = urllib2.build_opener()
        opener.addheaders = [(
          'User-agent',
          'python lingr(http://d.hatena.ne.jp/jYoshiori/)')]
        return opener

    def stream(self):
        self.create_session()
        self.get_rooms()
        self.subscribe()
        while True:
            obj = self.observe()
            if 'events' in obj:
                for event in obj['events']:
                    yield event
