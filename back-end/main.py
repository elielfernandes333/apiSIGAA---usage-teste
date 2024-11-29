from flask import Flask, redirect, request, session, url_for
import requests
import json

# Flask
server = Flask(__name__)
server.secret_key = 'sua_chave_secreta'

# APIconfig


# loginRouteAuth
@server.route('/auth/login', methods=['GET'])
def login():
    auth_url = (
        f"{URL_BASE_AUTENTICACAO}authz-server/oauth/authorize"
        f"?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
    )
    return redirect(auth_url)

# callbackRouteToReceiveCode
@server.route('/auth/callback', methods=['GET'])
def callback():
    # getAutorizationCode
    code = request.args.get('code')
    if not code:
        return "Código de autorização não recebido!", 400

    # switchAccessToken
    token_url = f"{URL_BASE_AUTENTICACAO}authz-server/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(token_url, data=data)
    token_response = response.json()

    if 'access_token' not in token_response:
        return f"Erro ao obter token: {token_response}", 400

    access_token = token_response['access_token']

    # getUserData
    user_info_url = f"{URL_BASE}usuario/{VERSION}/dados"
    headers = {'Authorization': f'Bearer {access_token}', 'x-api-key': x_api_key}
    user_info_response = requests.get(user_info_url, headers=headers)

    if user_info_response.status_code != 200:
        return f"Erro ao obter informações do usuário: {user_info_response.json()}", 400

    user_data = user_info_response.json()
    nome = user_data.get('nome', 'Desconhecido')
    email = user_data.get('email', 'Não informado')

    # saveData(opTeste)
    session['user'] = {'nome': nome, 'email': email}

    # homePageData(teste)
    return redirect(url_for('profile'))

# routeToShowUserProfile
@server.route('/profile', methods=['GET'])
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return f"Bem-vindo, {user['nome']}! Seu e-mail é {user['email']}."

if __name__ == '__main__':
    server.run(port=8081, debug=True)
