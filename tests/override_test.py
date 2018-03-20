""" Test boto3 client ovverride """
import os
import sys
import boto3
import placebo
from . import TestBase

# pylint: disable=wrong-import-order,wrong-import-position

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ssm_cache import SSMParameter

class TestClientOverride(TestBase):
    """ Refreshable.set_ssm_client tests """

    PLACEBO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'placebo/override'))

    def test_with_placebo(self):
        """ Test that set_ssm_client works fine with Placebo """
        session = boto3.Session()
        pill = placebo.attach(session, data_path=self.PLACEBO_PATH)
        pill.playback()

        client = session.client('ssm')

        SSMParameter.set_ssm_client(client)

        cache = SSMParameter("my_param")
        self.assertEqual(cache.value, "expected value")

        # reset to a proper client
        SSMParameter.set_ssm_client(boto3.Session().client('ssm'))

    def test_with_illegal_client(self):
        """ Test invalid client (without required methods) """
        with self.assertRaises(TypeError):
            SSMParameter.set_ssm_client(42)
