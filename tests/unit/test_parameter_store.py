from unittest import TestCase
from unittest.mock import patch

from botocore.exceptions import BotoCoreError, ClientError

from src.awstanding.parameter_store import DynamicParameter


@patch('src.awstanding.parameter_store._ssm_client.get_parameter')
class DynamicParameterTestCase(TestCase):
    def test_parameter_change(self, get_parameter_mock):
        ORIGINAL_VALUE = 'OriginalValue'
        get_parameter_mock.return_value = {'Parameter': {'Value': ORIGINAL_VALUE}}
        parameter = DynamicParameter('/test')

        self.assertEqual(parameter, ORIGINAL_VALUE)

        # A changed is produced on Parameter Store
        NEW_VALUE = 'NewValue'
        get_parameter_mock.return_value = {'Parameter': {'Value': NEW_VALUE}}

        self.assertEqual(parameter, NEW_VALUE)
        self.assertNotEqual(parameter, ORIGINAL_VALUE)

    def test_parameter_not_found(self, get_parameter_mock):
        get_parameter_mock.side_effect = ClientError(error_response={}, operation_name='fake operation')
        parameter = DynamicParameter('/test')

        with self.assertRaises(Exception):
            _ = parameter._value

        parameter = DynamicParameter('/test', fail_on_boto_error=False)

        self.assertEqual(parameter, '')
