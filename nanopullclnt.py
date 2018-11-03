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
A simple Python script, the client part of a pair of scripts to
test implementation of nanomsg PUSH/PULL between 1 server process
and a number of client processes.

Tested with nanomsg 1.1.4, nanomsg-python master (as of 1-Nov-18),
Python 2.7.15 on macOS Mojave 10.14
"""

from __future__ import print_function
import os
from nanomsg import poll, Socket, PUSH, PULL
from time import time
import sys
import argparse

parser = argparse.ArgumentParser(description='Extract parameters from command-line')
parser.add_argument('-cn', '--clientnumber', default = '1')
args = parser.parse_args()

client_number = int(args.clientnumber)

client_sock = Socket(PULL)
client_sock.connect('ipc://nanopushpull.bin')
timeout = 2 # seconds
not_finished = True
while not_finished:
  time_before_poll = time()
  r, _ = poll([client_sock], [], timeout)
  time_after_poll = time()
  if (time_after_poll - time_before_poll - timeout > 0):
    print("client #%d: timeout exceeded - no more messages?" % (client_number))
    break
  elif len(r) > 0:
    print("client #%d: got %s" % (client_number, client_sock.recv()))
  else:
    print("client #%d: something odd happened" % (client_number))
    break
client_sock.close()
