import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect

auth_url = "https://discord.com/api/oauth2/authorize?client_id=709321027775365150&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fuser%2F&response_type=code&scope=identify%20guilds"


def index(request):
    token = request.session.get('access_token')
    user = None
    guild = None
    if token:
        user, guild = getData(request.session['access_token'])
    return render(request, 'index.html', {'user': user, 'guild': guild})


def auth(request):
    token = request.session.get('access_token')
    if token:
        return redirect(user)
    return redirect(auth_url)


def user(request):
    token = request.session.get('access_token')
    if token:
        user, guild = getData(request.session['access_token'])
        admin_guilds = []
        for guilds in guild:
            perms = guilds['permissions']
            if perms & 8:
                admin_guilds.append(guilds)
        #return JsonResponse({'user': user, 'guild': admin_guilds})
        return render(request, 'user.html', {'user': user, 'guild': admin_guilds})

    code = request.GET.get('code')
    user, guild, access_token = exchange_code(code)

    request.session['access_token'] = access_token
    request.session['userID'] = user['id']

    return redirect(auth)


def logout(request):
    del request.session['access_token']
    del request.session['userID']
    return redirect(index)


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
        "client_secret": "Client Secret",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/user/",
        "scope": "identify guild"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']

    user, guild = getData(access_token)

    return user, guild, access_token


def commands(request):
    token = request.session.get('access_token')
    user = None
    guild = None
    if token:
        user, guild = getData(request.session['access_token'])
    return render(request, 'commands.html', {'user': user, 'guild': guild})


def docs(request):
    token = request.session.get('access_token')
    user = None
    guild = None
    if token:
        user, guild = getData(request.session['access_token'])
    return render(request, 'docs.html', {'user': user, 'guild': guild})

def dashboard(request):
    token = request.session.get('access_token')
    user = None
    guild = None
    guild_id = request.GET.get('ID')
    if token:
        user, guild = getData(request.session['access_token'])
        for guild_info in guild:
            if guild_info['id'] == guild_id:
                fetched_guild_info = guild_info
    return render(request, 'dashboard.html', {'user': user, 'guild': guild, 'guild_info': fetched_guild_info})
