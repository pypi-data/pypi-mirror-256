# CapBypassWrapped

`CapBypassWrapped` is a Python module that provides a wrapper for CapBypass, a captcha solving service. This module allows developers to easily integrate captcha solving functionality into their applications without having to write complex code.

## Installation

To install `CapBypassWrapped`, simply run the following command:

```
pip install CapBypassWrapped
```

## Usage

To use `CapBypassWrapped` functions, just import the module:

```python
import CapBypassWrapped
```

There are lots of different functions you can use with lots of customizability.

Here is every function below and how to initiate each one:

```python
def get_balance():
    result = CapBypassWrapped.get_balance(client_key="": str) # optional - verbose: bool
    print(result) # returns {"credits": str, "errorId": int}

def get_task_result():
    result = CapBypassWrapped.get_task_result(client_key="": str, task_id="": str) # optional - verbose: bool
    print(result) # returns {"solution": str, "status": str, "errorId": int}  

def create_funcaptcha_task():
    result = CapBypassWrapped.create_task(client_key="", task_type="", website_url="", website_public_key="") # optional - blob: str, verbose: bool
    print(result) # returns {"taskId": str}  

```

## License

`CapBypassWrapped` is licensed under the Apache License. See the LICENSE file for more information.

## Contact

If you have any questions or comments about `CapBypassWrapped`, please contact me on discord at @maxhithere
