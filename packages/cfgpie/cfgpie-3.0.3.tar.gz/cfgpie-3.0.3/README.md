# cfgpie

Simplified `ConfigParser` setup.

This module automates, to some extent, the setup of [ConfigParser](https://docs.python.org/3.7/library/configparser.html)
with cmd-line args parsing ability.

---

#### Installation:

```commandline
python -m pip install [--upgrade] cfgpie
```

---

#### Usage:

After installation, simply import the class `CfgParser` from `cfgpie` module:

```python
from cfgpie import CfgParser
```

By passing a name with the `name` param we can have multiple named instances:

```python
# mymodule.py

from cfgpie import CfgParser

cfg1: CfgParser = CfgParser(name="root")
cfg2: CfgParser = CfgParser(name="root")
cfg3: CfgParser = CfgParser(name="other")


if __name__ == '__main__':

    print("*" * 80)
    print("cfg1:", cfg1.name)
    print("cfg2:", cfg2.name)
    print("cfg3:", cfg3.name)

    print("*" * 80)
    print("cfg1 == cfg3:", cfg1 == cfg3)
    print("cfg1 is cfg3:", cfg1 is cfg3)

    print("*" * 80)
    print("cfg1 == cfg2:", cfg1 == cfg2)
    print("cfg1 is cfg2:", cfg1 is cfg2)
```

```
********************************************************************************
cfg1: root
cfg2: root
cfg3: other
********************************************************************************
cfg1 == cfg3: False
cfg1 is cfg3: False
********************************************************************************
cfg1 == cfg2: True
cfg1 is cfg2: True
```

Setting up our configuration:

```python
# -*- coding: UTF-8 -*-

from os.path import dirname, realpath, join
from sys import modules
from types import ModuleType

from cfgpie import CfgParser

# main python module:
MODULE: ModuleType = modules.get("__main__")

# root directory:
ROOT: str = dirname(realpath(MODULE.__file__))

# config default file path:
CONFIG: str = join(ROOT, "config", "config.ini")

BACKUP: dict = {
    "FOLDERS": {
        "logger": r"${DEFAULT:directory}\logs",  # extended interpolation
    },
    "TESTS": {
        "option_1": "some_value",
        "option_2": 23453,
        "option_3": True,
        "option_4": r"${DEFAULT:directory}\value",  # extended interpolation
        "option_5": ["abc", 345, 232.545, "3534.5435", True, {"key_": "value_"}, False],
    }
}

cfg: CfgParser = CfgParser(
    "root",
    defaults={"directory": ROOT}
)

# we can update `DEFAULT` section:
# cfg.set_defaults(directory=ROOT)

# we can provide a backup dictionary
# in case our config file does not exist
# and by default a new file will be created
cfg.open(
    file_path=CONFIG,
    encoding="UTF-8",
    fallback=BACKUP,
)


if __name__ == '__main__':

    # we're parsing cmd-line arguments
    cfg.read_argv()
    
    # cmd-args are fetched as a list of strings:
    # cfg.read_argv(["--tests-option_1", "another_value", "--tests-option_2", "6543"])

    print(cfg.get("TESTS", "option_1"))
    print(cfg.getint("TESTS", "option_2"))
```

For interpolation, refer to `interpolation-of-values`
[documentation](https://docs.python.org/3.7/library/configparser.html#interpolation-of-values).

To pass cmd-line arguments:

```commandline
python -O main.py --section-option value --section-option value
```
cmd-line args have priority over config file and will override the cfg params.

---

#### Defaults:

If not provided, by default, `CfgParser` will set:

* `defaults` parameter as dict with section `DEFAULT` and option `directory` to the root folder of the `__main__` module.


* `name` parameter to: `cfgpie`;


* `interpolation` parameter to [ExtendedInterpolation](https://docs.python.org/3.7/library/configparser.html#configparser.ExtendedInterpolation);


* `converters` parameter to evaluate:

    * `list`, `tuple`, `set` and `dict` objects using [ast.literal_eval()](https://docs.python.org/3.7/library/ast.html#ast.literal_eval) function;

    * `decimal` objects using [decimal.Decimal()](https://docs.python.org/3.7/library/decimal.html);

    * `path` strings using [os.path.realpath()](https://docs.python.org/3.7/library/os.path.html#os.path.realpath);

    * `folder` and `file` paths which:

        * return a path-like formatted string depending on the operating system;

        * will recursively create the folder structure if missing (see `folder()` & `file()` methods in [utils.py](src/cfgpie/utils.py)).

  > All of which can be accessed by prefixing them with `get`:
  >
  > * `getlist("SECTION", "option")`
  > * `gettuple("SECTION", "option")`
  > * `getset("SECTION", "option")`
  > * `getdict("SECTION", "option")`
  > * `getdecimal("SECTION", "option")`
  > * `getpath("SECTION", "option")`
  > * `getfolder("SECTION", "option")`
  > * `getfile("SECTION", "option")`

All other parameters are passed directly to
[ConfigParser](https://docs.python.org/3.7/library/configparser.html).

---
