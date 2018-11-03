# Copyright 2018 Jonathan Sherwin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A simple Python script, the server part of a pair of scripts to
test implementation of nanomsg PUSH/PULL between 1 server process
and a number of client processes.

Tested with nanomsg 1.1.4, nanomsg-python master (as of 1-Nov-18),
Python 2.7.15 on macOS Mojave 10.14
"""

from __future__ import print_function
import os
import sys
from nanomsg import poll, Socket, PUSH, PULL, DONTWAIT
import argparse
import subprocess
from time import sleep

parser = argparse.ArgumentParser(description='Extract parameters from command-line')
parser.add_argument('-cc', '--clientcount', default = '1')
parser.add_argument('-mc', '--messagecount', default = '1000')
args = parser.parse_args()

client_count = int(args.clientcount)
message_count = int(args.messagecount)

server_sock = Socket(PUSH)
server_sock.bind('ipc://nanopushpull.bin')

client_proc_list = []
for i in range(client_count):
  client_proc_list.append(subprocess.Popen(['python', 'nanopullclnt.py', '-cn', str(i+1)]))
# Give client processes time to start, otherwise the ones starting first will
# get hit with a big chunk of the messages (which may not be a bad thing)
sleep(1)

for n in range(message_count):
  sent = False
  while not sent:
    try:
      server_sock.send(b'msg %d' % (n), DONTWAIT)
      sys.stdout.write('!')
      sys.stdout.flush()
      sent = True
    except:
      # Seems like no clients are currently connnected
      sys.stdout.write('.')
      sys.stdout.flush()

for client_proc in client_proc_list:
  poll = client_proc.poll()
  while poll is None:
     sleep(1)
     poll = client_proc.poll()
print("...finis...")
server_sock.close()
