import json

import requests
from django.shortcuts import render
from .models import Team, ASUser, headers


def home(requset):
    return render(requset, 'base.html')

def get_users(request):
    team = Team.objects.first()
    user_url = 'https://app.asana.com/api/1.0/teams/' + str(team.team_gid) + '/users'
    r = requests.get(user_url, headers=headers)
    data = json.loads(r.text)


    for user in data['data']:
        u = ASUser.objects.create(
            name=user['name'],
            as_user_gid=user['gid']
        )
        u.save()
        a = 1
        a = a + 1
        if a == 3:
            break
    return render(request, 'base.html')



