# parktain
A slack bot for the park-ers

## Before you install

Create a virtualenv and activate it(recommended):

    virtualenv mydir
    cd mydir
    source activate/bin

Upgrade pip:

    pip install --upgrade pip    

Clone the repository:

    git clone https://github.com/punchagan/parktain.git
    cd parktain/

## Installation

To install dependencies:

    pip install -r requirements.txt

To install the bot:

    python setup.py install


To setup the bot for development, run:

    python setup.py develop

## Setup

Change directory into your slackbot folder(here, parktain):

    cd parktain/
    
Find Slack API token for your @<botname> here:

    https://my.slack.com/services/new/bot

Paste the following as is into config.yaml(or create it):

    gendo:
      auth_token: "API-token-from-previous-step"

## Run

To run your bot:
    python main.py