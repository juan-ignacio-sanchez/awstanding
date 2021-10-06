"""Parameter Store Loader
Use (setting_name, cast function) or setting_name as lookup value.
If no cast function is passed, the parameter will be stored as retrieved
from Parameter Store, typically string or stringList.

Usage:
from awstanding.parameter_store import load_parameters

LOOKUP_DICT = {
    '/my/parameter/path': 'NEW_VARIABLE'
}

load_parameters(LOOKUP_DICT)

# Now NEW_VARIABLE can be obtained from environment variables.

"""
import os
import boto3


def load_parameters(lookup_dict):
    ssm = boto3.client(service_name='ssm')
    paginated_keys = (list(lookup_dict.keys())[i:i+10] for i in range(0, len(lookup_dict), 10))

    parameters_ps = []
    invalid_parameters = []
    for keys in paginated_keys:
        parameters_page = ssm.get_parameters(Names=keys, WithDecryption=True)
        parameters_ps += parameters_page['Parameters']
        invalid_parameters += parameters_page['InvalidParameters']

    parameters_ps = {param['Name']: param['Value'] for param in parameters_ps}

    # Override configuration for requested keys
    for key in parameters_ps:
        if isinstance(lookup_dict[key], (tuple, list)):
            setting_name, cast = lookup_dict[key]
            os.environ[setting_name] = cast(parameters_ps[key])
        elif isinstance(lookup_dict[key], str):
            os.environ[lookup_dict[key]] = parameters_ps[key]
