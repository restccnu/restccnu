# coding: utf-8

import sys
from mock.app import mock_app
from restccnu import app
from gevent import monkey
monkey.patch_all()


def run_server(host="0.0.0.0", port="5060"):
    """run develop server"""
    app.run(debug=True, host=host, port=int(port))


def run_mock_server(host="0.0.0.0", port="5060"):
    """run mock develop server"""
    mock_app.run(debug=True, host=host, port=int(port))


def restccnu_test():
    """run unit test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')  # discover tests
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    # start: python manage.py runserver/mock host:port
    if len(sys.argv) > 1 and sys.argv[1] == 'mock':
        if len(sys.argv) > 2:
            path = sys.argv[2]
            host, port = path.split(':')
        run_mock_server(host, port)

    elif len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        if len(sys.argv) > 2:
            path = sys.argv[2]
            host, port = path.split(':')
        run_server(host, port)

    elif len(sys.argv) > 1 and sys.argv[1] == 'test':
        restccnu_test()
