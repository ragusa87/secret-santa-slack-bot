# Secret Santa Slack Bot

The bot takes all the users in a specific channel and add them to the specified user group.

Why ?
> So in the Secret Santa app <https://secret-santa.team/>, you can select the group and all the users from this group will be added. (As it's not possible to do so with a #channel)



## Requirements - Install
- Python 3
- virtualenv starterbot
- source starterbot/bin/activate
- slack_sdk: ```pip install slack_sdk```
- cp .env.dist .env

## Setup
1. Create a new App within your Slack workspace: https://api.slack.com/apps
2. Add some Scope to your app
- groups:write
- channels:read
- usergroups:read
- users.profile:read

3. Put your token in the .env
4. Go on slack and create a new user group
5. Find the created group id (by inspectring the query or via api)
6. Edit your .env to update the GROUP_ID

## Usage
1. Import .env `export $(cat .env)`
2. Run the script `python3 ./secret_santa.py`
3. Open the secret Santa app, click on the group that you want to use.

## .env file
```
## Environment variables
`SLACK_API_TOKEN`: your slack bot access token - Required.
`GROUP_NAME`: Your group name - Required.
`CHANNEL_NAME`: the name of your secret santa channel - Optional. Default: secret-santa
