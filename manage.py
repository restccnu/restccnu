# coding: utf-8

import sys
from mock.app import mock_app


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'mock':
        mock_app.run(debug=True)
