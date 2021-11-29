import os
import pprint
import requests
import json

pp = pprint.PrettyPrinter(indent=4)

from slack_sdk import WebClient

client = WebClient(token=os.environ['SLACK_API_TOKEN'])

group_name = os.environ.get("GROUP_NAME", "SecretSanta")
channel_name = os.environ.get("CHANNEL_NAME", "secret-santa")
debug = os.environ.get("Debug", True)


def get_channel_id_by_name(secret_santa_channel_name: str):
    # https://api.slack.com/methods/conversations.members
    # channels:read,groups:read,mpim:read,im:read, mpim:read
    channels = []
    print("Fetching channels list")
    for page in client.conversations_list(limit=500):
        channels = channels + page["channels"]
    for channel in channels:
        if channel["name"] == secret_santa_channel_name:
            print("Channel %s found as id %s" % (secret_santa_channel_name , channel["id"]))
            return channel["id"]
    raise NameError("Channel %s not found" % secret_santa_channel_name)

def get_channel_members(channel_id: str):
  
    users = []
    print("Fetching users for channel %s" % channel_id)
    for page in client.conversations_members(channel=channel_id,limit=500):
        users = users + page["members"]
    return users


def update_group_members(users: [], group_id: str):
    # https://api.slack.com/methods/usergroups.users.update
    # usergroups:write
    r = client.usergroups_users_update(users=",".join(users), usergroup=group_id)
    if r.status_code != 200:
        raise NameError("Error")
    return True

# usergroups:read
def get_usergroup_id_from_name(group_name: str):

    # https://api.slack.com/methods/usergroups.list
    groups = []
    print("Fetching groups ")
    for page in client.usergroups_list(limit=100):
        groups = groups + page["usergroups"]

    print("Looking for group %s" % group_name)
    for g in groups:
        if g["name"] == group_name:
            print("Group %s found as id %s" % (group_name , g["id"]))
            return g["id"]

    raise NameError("No group found with name %s" % group_name) 



channel_id = os.environ.get("CHANNEL_ID", None)
if channel_id is None:
    channel_id = get_channel_id_by_name(channel_name)


group_id = os.environ.get("GROUP_ID")
if group_id is None:
    group_id = get_usergroup_id_from_name(group_name)


members = get_channel_members(channel_id)
print("Found %s members in channel %s (%s). Note that apps & bots are included" % (len(members), channel_id, channel_name))
print("Adding the users in group %s" % group_id)

update_group_members(members, group_id)

exit(0)
