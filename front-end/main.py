from flask import Flask, render_template      # type: ignore

server = Flask(__name__)

@server.route('/', methods=['GET'])
def index() -> str:
    return render_template('index.html')

@server.route('/profile', methods=['GET'])
def profile() -> str:
    return render_template('profile.html', user_name = 'Volkof Aleksey', user_email = 'alekseyVolkof@mail.com')





if __name__ == '__main__':
    server.run(port=8080, debug=True, ssl_context='adhoc');


