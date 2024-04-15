# write tests for main.py

# Path: test.py
import json
import unittest
from flask import Flask, g
from flask_oidc import OpenIDConnect


class TestFlaskOidc(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # test the loging redirect from main.py
    def test_hello_world(self):
        # test the loging redirect from main.py
        from main import app
        with app.test_client() as c:
            redirect = c.get('/')
            assert redirect.status_code == 302

    def test_hello_me(self):
        # test anonymous user access to /private
        from main import app
        with app.test_client() as c:
            response = c.get('/private')
            assert response.status_code == 302

    def test_hello_api(self):
        # test a bad configuration file in app.config
        from main import app
        app.config.update({})
        with app.test_client() as c:
            response = c.get('/api')
            assert response.status_code == 500

    def test_logout(self):
        pass


def deep_update(orignal_dict, update_dict):
    for k, v in update_dict.items():
        if isinstance(v, dict):
            orignal_dict[k] = deep_update(orignal_dict.get(k, {}), v)
        else:
            orignal_dict[k] = v
    return orignal_dict


def load_config(config_file):
    with open(config_file) as f:
        config = json.load(f)
    return config


if __name__ == '__main__':
    unittest.main()
