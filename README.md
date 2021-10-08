# AWStanding
Easily load variables from AWS Parameter store into environment variables.

# Why to AWStanding?
Because it handles AWS pagination so the amount of requests performed to retrieve the parameters are the bare minimum.
Also it handles invalid parameters, so you don't have to deal with undefined variables exceptions, as an option. 

# Installation

```shell script
pip install awstanding
```

I personally recommend using pipenv:
```shell script
pipenv install awstanding
```

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

# Performance

| Amount of parameters | Missing parameters | AWStanding | SSM client calls |
| --- | --- | --- | ---|
| 40 | 0 | ~3.1s| ~15.5s |
| 40 | 0 | ~2.4s| ~15.3s |
| 40 | 0 | ~4.6s| ~14.5s |
| 40 | 0 | ~2.5s| ~15.5s |
| 40 | 1 | ~2.1s| error: ParameterNotFound |
| 40 | 20 | ~2.2s| error: ParameterNotFound |
| 40 | 40 | ~2.1s| error: ParameterNotFound |
| 80 | 40 | ~3.5s| error: ParameterNotFound |
| 80 | 40 | ~3.9s| (using try..except) ~32.7s |

# Loading paths
Suppose you have defined these variables in ParameterStore:
```python
'/stripe/price/'
'/stripe/webhook/'  # (Let's not define this one just for demonstration)
```
You can leverage on the good naming and perform a path variable loading as follows:

```python
import os
from awstanding.parameter_store import load_path

load_path('/stripe', '/spotify')
STRIPE_PRICE = os.environ.get('STRIPE_PRICE', 'fallback_value')
STRIPE_WEBHOOK = os.environ.get('STRIPE_WEBHOOK', 'fallback_value')
SPOTIFY_API_KEY = os.environ.get('SPOTIFY_API_KEY', 'fallback_value')

print(f'price: {STRIPE_PRICE}, webhook: {STRIPE_WEBHOOK}, spotify: {SPOTIFY_API_KEY}')

>>> price: price_1xxxxxxxxxxxxxxxxxxxxxxx, webhook: fallback_value, spotify: fallback_value
```

# Dynamic Parameters

You can define dynamic parameters that uploads themselves each time they are used, so you can update
any parameter without re-deploy your service.

```python
from awstanding.parameter_store import DynamicParameter

IMPORTANT_SETTING = DynamicParameter('/test/parameter')

print(IMPORTANT_SETTING)
>>> OriginalValue

# Someone updates /test/parameter on AWS...

print(IMPORTANT_SETTING)
>>> NewValue
```

## Supported operations

Some useful operations are supported by the class itself, emulating built-in str class:

```python
from awstanding.parameter_store import DynamicParameter

IMPORTANT_SETTING = DynamicParameter('/test/parameter')

# Equality comparison
equal = IMPORTANT_SETTING == 'SomeString'

# Length
length = len(IMPORTANT_SETTING)

# Concatenation (Right and Left)
concat = '~' + IMPORTANT_SETTING + '~'

# You can always convert the parameter to string to get full string capabilities:

str_IMPORTANT_SETTING = str(IMPORTANT_SETTING)  # Have in mind this will "freeze" the value, so don't overwrite IMPORTANT_SETTING
```
