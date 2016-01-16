## Introduction
Quotedian is a social media reputation bot for Twitter and Instagram running on Google App Engine

## Requirements
* Python 2.7
* Google App Engine SDK

## Install
Run 'pip install -r requirements.txt -t lib/' to install these dependencies  in lib/ subdirectory.

## Twitter API Instructions
* Register as a developer with Twitter
* Create new app and note API keys

## Config
Rename sample_settings.cfg to settings.cfg and fill in API keys and other info
SEARCH TERMS: add a comma delimited list of search terms that the bot will retweet.  Hint - the bot will randomly pick from this list, so repeating a term will increase its liklihood of being matched 

## App Engine Instructions
* Create new app
* Replace application name at top of app.yaml

### Scheduling Bot Execution on GAE
Update bot execution frequency in cron.yaml

### Deployment
Deploy using App Engine launcher