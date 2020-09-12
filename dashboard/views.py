import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect

auth_url = "https://discord.com/api/oauth2/authorize?client_id=709321027775365150&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fuser%2F&response_type=code&scope=identify%20email%20guilds"


def index(request):
    return render(request, 'index.html')


def auth(request):
    if request.session['access_token']:
        return redirect(user)
    else:
        return redirect(auth_url)


def user(request):
    if request.session['access_token']:
        user, guild = getData(request.session['access_token'])

        return JsonResponse({'user': user, 'guild': guild})

    code = request.GET.get('code')
    user, guild, access_token = exchange_code(code)

    request.session['access_token'] = access_token
    request.session['userID'] = user['id']

    return JsonResponse({'user': user, 'guild': guild})


def getData(access_token):
    user_response = requests.get("https://discord.com/api/v6/users/@me", headers={
        'Authorization': 'Bearer %s' % access_token
    })
    guild_response = requests.get("https://discord.com/api/v6/users/@me/guilds", headers={
        'Authorization': 'Bearer %s' % access_token
    })

    return user_response.json(), guild_response.json()


def exchange_code(code: str):
    data = {
        "client_id": "709321027775365150",
        "client_secret": "I_7XyaUS-4QmW5ttSd8lNNt2XXCxd5U6",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/user/",
        "scope": "identify email guild"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']

    user, guild = getData(access_token)

    return user, guild, access_token
