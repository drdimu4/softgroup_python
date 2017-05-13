import json
import requests

# data = requests.post('http://localhost:5000/api/all_posts')
#
# with open('data.txt', 'w') as outfile:
#     json.dump(data.json(), outfile)
#
# logs = requests.post('http://localhost:5000/api/all_logs')
#
# with open('logs.txt', 'w') as outfile:
#     json.dump(logs.json(), outfile)
#
users = requests.post('http://localhost:5000/api/all_user')

with open('users.txt', 'w') as outfile:
    json.dump(users.json(), outfile)