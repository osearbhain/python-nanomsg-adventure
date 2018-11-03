# python-nanomsg-adventure
Experiments with nanomsg using Python

<h2>nanopushsrvr.py, nanopullsrvr.py</h2>

Requires:
  
- nanomsg (https://nanomsg.org) - on macOS, install with Homebrew (https://brew.sh):
    
      brew install nanomsg
      
- nanomsg-python (https://github.com/tonysimpson/nanomsg-python) - on macOS:
    
      git clone https://github.com/tonysimpson/nanomsg-python    
      cd nanomsg-python
      python setup.py build
      python setup.py install

Then try it with, e.g. for 10 client processes pulling 1000 messages from the server:

      python nanopushsrvr.py -cc 10 -mc 1000
