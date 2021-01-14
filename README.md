# metpx-cloud-publisher

## Overview

MetPX-Sarracenia plugin for publishing data to the cloud

## Installation

### Requirements
- Python 3
- [virtualenv](https://virtualenv.pypa.io/)

### Dependencies
Dependencies are listed in [requirements.txt](requirements.txt). Dependencies
are automatically installed during metpx-cloud-publisher installation.

### Installing metpx-cloud-publisher

```bash
# setup virtualenv
python3 -m venv --system-site-packages metpx-cloud-publisher
cd metpx-cloud-publisher
source bin/activate

# clone codebase and install
git clone https://github.com/wmo-cop/metpx-cloud-publisher.git
cd metpx-cloud-publisher
pip3 install -r requirements.txt

# configure environment
cp metpx-cloud-publisher.env dev.env
vi dev.env  # update Azure credentials and path to MetPX filter
. dev.env

vi metpx-cloud-publisher.conf  # adjust on_file path and desired subtopics
```

## Running

```bash
sr_subscribe foreground metpx-cloud-publisher.conf
```

## Development

### Code Conventions

* [PEP8](https://www.python.org/dev/peps/pep-0008)

### Bugs and Issues

All bugs, enhancements and issues are managed on [GitHub](https://github.com/wmo-cop/metpx-cloud-publisher/issues).

## Contact

* [Tom Kralidis](https://github.com/tomkralidis)
