import unittest
import requests

try:
    import flask
except:
    flask = None

from . import *

import logging
logger = logging.getLogger(__name__)


class FlaskUtilTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if flask is None:
            raise unittest.SkipTest('flask not installed')

    def test_flask_util(self):
        self.assertEqual(1, 1)

    # TODO: Spin up a server instance
    # Maybe using with?
    # Destroy it with the test destructor

    #def test_batch