import json
import logging

from flask import Flask, g
from flask_oidc import OpenIDConnect

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

is_okta = False

OKTA = "https://dev-209322.okta.com"
ICP = 'https://wcnda2.localhost.illumina.com:5000/oidc_callback'

app.config.update({
    'OIDC_USER_INFO_ENABLED': True,
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json' if is_okta else 'client_secrets_icp.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    # 'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_OPENID_REALM': OKTA if is_okta else ICP
    # 'OIDC_VALID_ISSUERS': ['https://dev-209322.okta.com', 'https://platform.login.testing-domain.illumina.com',
    #                        'https://platform.login.testing-domain.illumina.com/platform-services-manager',
    #                        'http://platform.us.informatics.illumina.com:8080/platform-services-manager']
})
oidc = OpenIDConnect(app)


@app.route('/')
def hello_world():
    if oidc.user_loggedin:
        return ('Hello, %s, <a href="/private">See private</a> '
                '<a href="/logout">Log out</a>') % \
            oidc.user_getfield('email')
    else:
        return 'Welcome anonymous, <a href="/private">Log in</a>'


@app.route('/private')
@oidc.require_login
def hello_me():
    info = oidc.user_getinfo(['email', 'sub', 'addr_country'])
    return ('Hello, %s (%s)! [%s] <a href="/">Return</a>' %
            (info.get('email'), info.get('sub'), info.get('addr_country')))


@app.route('/api')
@oidc.accept_token(True, ['openid'])
def hello_api():
    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})


@app.route('/logout')
def logout():
    oidc.logout()
    return 'Hi, you have been logged out! <a href="/">Return</a>'


if __name__ == '__main__':
    # host = 'wcnda2.localhost.illumina.com'
    host = 'localhost' if is_okta else 'wcnda2.localhost.illumina.com'
    ssl_context = None if is_okta else 'adhoc'
    app.run(host=host, port=5000, debug=True, ssl_context=ssl_context)
