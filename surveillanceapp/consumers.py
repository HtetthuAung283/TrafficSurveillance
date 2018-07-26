from channels import Group, channel
import json
import time
import cv2
import random
import multiprocessing
from multiprocessing.managers import BaseManager
from . import cvrender, videoplayer
import numpy as np
import os
from django.conf import settings


class MyChannel(channel.Channel):

    def __init__(self,name):
        super(MyChannel, self).__init__(name)
        print('My Channel created with name {}'.format(name))
        print(self.name)
        print(self.channel_layer)

    def send(self, content, immediately=True):
        print('Sending from my channel')
        super(MyChannel, self).send(content, immediately)

    def set(self,value):
        self.value = value

    def get(self):
        print(self.value)


def testfunc(returnchannel):
    # print('Channel layer: ', returnchannel.channel_layer)
    # print('Channel name: ', returnchannel.name)
    # customchannel = MyChannel(returnchannel.name)   # Use channel layer also in next try!
    returnchannel.send({
        'text': json.dumps({
            'eof': True,
            'message': 'The video stream has ended'
        })
    }, True)

    returnchannel.set('Hello world')


def ws_connect(message,videoid):
    print(message)
    Group('users').add(message.reply_channel)
    message.reply_channel.send({
        'accept': True
    })


def ws_receive(message,videoid):
    print('A message has arrived')
    print(message.reply_channel)
    received = json.loads(message.content.get('text'))
    if received['start']:
        videopath = os.path.join(settings.BASE_DIR,'testvideos/ratnapark.MOV')   # This is the place where we find the address of the video
        videoplayer.runvideo(videopath, message.reply_channel)
        print('This must be printed after the video has been closed and returned to consumer')


def ws_disconnect(message,videoid):
    print('Socket has now been disconnected: ',message.reply_channel.name)
    Group('users').discard(message.reply_channel)
