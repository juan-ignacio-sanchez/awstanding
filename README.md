# AWStanding
Easily load variables from AWS Parameter store into environment variables.

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
