#!/usr/bin/env python
import todoist
import json
import sys
import os

# load config
try:
    with open(os.path.join(os.path.expanduser('~'), '.task', 'hooks', 'config.json'), 'r') as configFile:
        config = json.load(configFile)
except Exception:
    print('Failed to load config.')
    sys.exit(1)

# capture input
pre_task = json.loads(sys.stdin.readline())
post_task = json.loads(sys.stdin.readline())

# check that config is correct
if not 'user' in config or not 'username' in config['user'] or not 'password' in config['user']:
    print('Failed to read config properly. Can''t upload to Todoist.')
else:
    # connect to todoist
    api = todoist.TodoistAPI()
    user = api.user.login(config['user']['username'], config['user']['password'])
    api.sync()
    # check if the task was completed.
    if not pre_task['status'] == 'completed' and post_task['status'] == 'completed':
        try:
            item = api.items.get_by_id(int(post_task['tdi_uuid']))
            item.complete()
            api.commit()
        except KeyError:
            print('Failed to complete task on Todoist. Looks like it was missing its Todoist ID.')
            sys.exit(1)
        print('Task completed on Todoist.')
    # check if the task was deleted.
    elif not pre_task['status'] == 'deleted' and post_task['status'] == 'deleted':
        try:
            item = api.items.get_by_id(int(post_task['tdi_uuid']))
            item.delete()
            api.commit()
        except KeyError:
            print('Failed to delete task on Todoist. Looks like it was missing its Todoist ID.')
            sys.exit(1)
        print('Task deleted on Todoist.')

# write out the task to taskwarrior
print(json.dumps(post_task))
sys.exit(0)
