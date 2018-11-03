# python-nanomsg-adventure
Experiments with nanomsg using Python

nanopushsrvr.py, nanopullsrvr.py
  requires:
    nanomsg (https://nanomsg.org) - on macOS, install with Homebrew (https://brew.sh):
      brew install nanomsg
    nanomsg-python (https://github.com/tonysimpson/nanomsg-python) - on macOS:
      git clone https://github.com/tonysimpson/nanomsg-python
      cd nanomsg-python
      python setup.py build
      python setup.py install
