[![codecov](https://codecov.io/gh/remiflavien1/awesome-check-link/branch/master/graph/badge.svg)](https://codecov.io/gh/remiflavien1/awesome-check-link)  [![PyPI version](https://badge.fury.io/py/awesome-check-link.svg)](https://badge.fury.io/py/awesome-check-link) [![Requirements Status](https://requires.io/github/remiflavien1/awesome-check-link/requirements.svg?branch=master)](https://requires.io/github/remiflavien1/awesome-check-link/requirements/?branch=master) [![Code Coverage](https://github.com/remiflavien1/awesome-check-link/workflows/Code%20coverage/badge.svg)](https://github.com/remiflavien1/awesome-check-link/actions?query=workflow%3A%22Code+coverage%22) [![Quality check](https://github.com/remiflavien1/awesome-check-link/workflows/Quality%20check/badge.svg)](https://github.com/remiflavien1/awesome-check-link/actions?query=workflow%3A%22Quality+check%22)

# awesome-check-link

Check if links in md file and more particularly in awesome-list are down or not.

## Install

You can install ```awesome-check-link``` either via pip (PyPI) or from source.
```bash
python3 -m pip install awesome-check-link
```
Or manually:
```
git clone https://github.com/remiflavien1/awesome-check-link
cd awesome-check-link
python3 setup.py install
```

To upgrade ```aclinks```: 
```sh
python3 -m pip  install --upgrade awesome-check-link
```

## Usage
### CLI 

```sh
$ aclinks --help  
Awesome Check Links 

Usage:
    aclinks [--verbose --exit --down] -f FILE
    aclinks (-h | --help | --version)

Options:
    -f --file       Markdown file to scan.
    -e --exit       Stop and raise error if a site is down.
    -d --down       Show only down links and their line number.
    -v --verbose    Verbose mode. Print more to stdout.
    -h --help       Show this help.
    --version       Show version.
```

Example of output for the [Awesome-anti-forensic](https://github.com/remiflavien1/awesome-anti-forensic)
```sh
$ git clone https://github.com/remiflavien1/awesome-anti-forensic
$ cd awesome-anti-forensic
$ aclinks -vd -f README.md # only display down links

At line 24 : https://www.paterva.com/web7/buy/maltego-clients/casefile.php : Moved Permanently ( 301 )
At line 61 : https://www.bishopfox.com/resources/tools/other-free-tools/mafia/ : Moved Permanently ( 301 )
At line 64 : https://www.paterva.com/web7/buy/maltego-clients/maltego-ce.php : Moved Permanently ( 301 )
```

With exit mode (```--exit flag```), exit the program if one link is down. Can be integrated in a CI/CD workflow.

## License

[MIT](LICENSE)
