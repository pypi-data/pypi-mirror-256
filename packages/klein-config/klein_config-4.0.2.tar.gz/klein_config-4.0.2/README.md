# Klein Config

Module to provide config management

## Usage

```python
from klein_config import get_config

# Can be overriden with env variable MY_CONFIG_SETTING
config = get_config({"my": {"config": {"setting": "initialised value"}})

# Access via `get` accessor with no backup (raises ConfigMissingException if not found).
value = config.get("my.config.setting")

# Access via `get` accessor method with a backup.
backup_value = config.get("not.a.setting", "backup value")

# Access via `dict` (raises KeyError if not found).
same_value = config["my.config.setting"]

# Sub-configs are created if the value is another `dict`.
intermediate_config = config["my.config"]
same_value_again = intermediate_config["setting"]
```

### Structure
Internally the config object uses the ConfigTree structure that is part of pyhocon. This can be traversed easily with the get method using dot notation as outlined above.

### Config Initialisation
The `get_config` function looks for :
- argument `--common` or environmental variable `KLEIN_COMMON` to specify a valid filepath for a common config file (in either JSON or YAML format); and
- argument `--config` or environmental variable `KLEIN_CONFIG` to specify a valid filepath for a config file 


N.B. Passing both environmental variables _and_ arguments for either config or common is ambiguous and is therefore NOT accepted.

You can also pass a `dict` into the `get_config` function.

#### Example configs
JSON:
```json
{
  "rabbitmq": {
    "host": [
      "localhost"
    ],
    "port": 5672,
    "username": "username",
    "password": "password"
  },
  "mongo": {
    "host": [
      "mongo.domain.com"
    ],
    "username": "username",
    "password": "password"
  }
}
```
YAML:
```yaml
mongo:
  host:
    - mongo.domain.com
  password: password
  username: username
rabbitmq:
  host:
    - localhost
  password: username
  port: 5672
  username: password
```

Example config files are also provided in [json](example.config.json) and [yaml](example.config.yaml) formats.

### Order precedence
The configs are applied to the config object in the following order: 

1. Common config as identified via argument `--common` or environmental variable `KLEIN_COMMON`
2. Config that is injected via the Class constructor
3. Config that is identified via the argument `--config` or environmental variable `KLEIN_CONFIG`


Configs will override any previous values as they are applied.

### Environment Aware
The module is "Environment Aware", i.e. it will look for environment variables in the first instance. If a valid variable exists then this will be used regardless of any config that may have been supplied.

The path is transformed by converting the string to uppercase and replacing all dots with underscores.

```
my.config.setting => MY_CONFIG_SETTING
```

Sub-config items are still overriden by the same environment variables as in the root config.

## Development
This project uses [pipenv](https://github.com/pypa/pipenv). To install it, run `pip install pipenv`.

### Development
```
pipenv install --dev
```

### Testing
```bash
pipenv run python -m pytest
```
For test coverage you can run:
```bash
pipenv shell
pipenv run python -m pytest --cov-report term --cov src/ tests/
```

## Unit testing config in another library.
You need to monkey patch the config library and override what the methods do in your test code.
First create your test version of config. Let's say it is in the module `tests.test_config`.

```python
from klein_config.config import EnvironmentAwareConfig

config_dict = {
    'consumer': {
        'name': 'text_classifier',
        'queue': 'text_classifier',
    },
    'mongo': {
        'host': 'localhost',
        'port': 27017,
        'doclib_database': 'doclib',
        'documents_collection': 'documents',
        'text_classification_collection': 'text_classification',
    }
}

config = EnvironmentAwareConfig(initial=config_dict)

def get_config():
    return config

```
Then in your test code you can monkey patch the config library like this:

```python
import sys
sys.modules['klein_config'] = __import__('tests.test_config')

from tests.test_config import config
```
Now any test code that uses klein_config will use this test version of the config library.

### Troubleshooting

If you are unable to run `pipenv shell` and are having permission errors, you can spin up a virtual environment in which to run 
the `pipenv` commands:

```bash
pip install virtualenv      // install virtualenv module
virtual env venv            // create your virtual environment (run command from project root directory)
source venv/bin/activate    // start the virtual environment
pipenv install --dev        // install dependencies - you should now be able to run the tests with the above commands
```

### Known issue

#### Library does not install on some python versions.
This issue has appeared on a few occasions due to a tagged dependency on pyyaml. This library requires certain version of python to install. 

If this library does not install on pyyaml failure, you can still install and use this library with using --no-deps flag and manually install the dependencies. 

```
pip install --no-deps klein_config   # Don't forget to install the dependencies as needed
```


### License
This project is licensed under the terms of the Apache 2 license, which can be found in the repository as `LICENSE.txt`
