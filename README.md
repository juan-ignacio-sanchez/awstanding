# AWStanding
Easily load variables from AWS Parameter store into environment variables.

# Why to AWStanding?
Because it handles AWS pagination so the amount of requests performed to retrieve the parameters are the bare minimum.
Also it handles invalid parameters, so you don't have to deal with undefined variables exceptions, as an option. 

# Quickstart
```python
from awstanding.parameter_store import load_parameters
load_parameters({'/some/path/to/something/stored': 'IMPORTANT_SETTING'})

import os
print(os.environ.get('IMPORTANT_SETTING'))
'super-important-value'
```

# Using with python-decouple
```python
import os
from awstanding.parameter_store import load_parameters
from decouple import config
load_parameters({'/some/path/to/something/stored': 'IMPORTANT_SETTING'})

IMPORTANT_SETTING = config('IMPORTANT_SETTING', default='some-default')
print(IMPORTANT_SETTING)
'super-important-value'
```

# Not allowing missing parameters
```python
from awstanding.parameter_store import load_parameters
# A call like this one:
load_parameters({'/not/defined/parameter': 'IMPORTANT_SETTING'}, allow_invalid=False)

# will raise a ParameterNotFoundException, and you can handle it as follows:
from awstanding.exceptions import ParameterNotFoundException

try:
    load_parameters({'/not/defined/parameter': 'IMPORTANT_SETTING'}, allow_invalid=False)
except ParameterNotFoundException as e:
    # perform any cleanup action..
```