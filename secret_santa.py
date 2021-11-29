import os
import pprint
import requests
import json

pp = pprint.PrettyPrinter(indent=4)

from slack_sdk import WebClient

client = WebClient(token=os.environ['SLACK_API_TOKEN'])

dry_run = True


def get_channel_members(secret_santa_channel_name: str):
    if dry_run:
        return ["u1","u2","u3"]

    # https://api.slack.com/methods/conversations.members
    # channels:read,groups:read,mpim:read,im:read, mpim:read
    response = client.conversations_members(channel=secret_santa_channel_name,limit=500)
    return r.get("members")


def update_group_members(users, group_id: str):
    if dry_run:
        return

    # https://api.slack.com/methods/usergroups.users.update
    # usergroups:write
    r = client.usergroups_users_update(users=",".join(users), usergroup=group_id)
    pp.pprint(r)

# usergroups:read
def get_usergroup_id_from_name(group_name: str):
    if dry_run:
        return "42_"+ group_name
    # https://api.slack.com/methods/usergroups.list
    r = client.usergroups_list()
    for g in r.get("usergroups"):
         if g.name == group_name:
            return g.id
    raise NameError(f"No group found with name :" % group_name) 

group_id = get_usergroup_id_from_name(os.environ.get("GROUP_NAME", "secretsanta"))
members = get_channel_members(os.environ.get("CHANNEL_NAME", "secret-santa"))
pp.pprint(group_id)
pp.pprint(members)

update_group_members(members, group_id)

exit(0)
