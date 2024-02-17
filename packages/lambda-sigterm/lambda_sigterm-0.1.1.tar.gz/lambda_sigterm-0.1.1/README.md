# Lambda SIGTERM - Allows graceful shutdown of Lambdas using Python

The [Lambda Extensions API](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html) allows lambdas to register extensions. Once an extension is registered, the Lambda runtime will send a SIGTERM to the function code so the extension can collect metrics, etc.

What if you want the benefits of getting SIGTERM signals without the overhead of third-party extensions which collect metrics? Use `lambda-sigterm`!

This library creates a noop extension. All the extension does is register itself with the Lambda Extensions API, then blocks on a background thread. This makes it so the Lambda handler will receive SIGTERM signals. The library code uses `urllib3` (included with the Lambda Python runtime) and Python stdlib libraries, so there are no external dependencies in the Lambda environment.

## Installation
```bash
$ pip install lambda_sigterm
```

## How To Use
To use, import the `lambda_sigterm` module and call the `register()` function:

```python
import signal
import lambda_sigterm

lambda_sigterm.register()

def handle_sigterm(signum, frame):
    print("sigterm captured")

signal.signal(signal.SIGTERM, handle_sigterm)
```

## Full Example

```python
import signal
import lambda_sigterm

lambda_sigterm.register()

def handle_sigterm(signum, frame):
    print("sigterm captured")

signal.signal(signal.SIGTERM, handle_sigterm)

def lambda_handler(event, context):
    print("your application code has started")
```

## `register` Arguments
| keyword_arg | default | description | example |
|---|---|---|---|
| `logger` | `None` | a `logging` `Logger` to use, creates a new logger if none (falsy) is supplied | `logging.getLogger('myapp')` |
| `log_level` | `logging.ERROR` | log-level for the logger if none is supplied | `logging.INFO` |
| `log_level_debug_msg` | `logging.DEBUG` | log-level for debug logs |  |
| `log_level_info_msg` | `logging.INFO` | log-level for info logs |  |
| `log_level_error_msg` | `logging.ERROR` | log-level for error logs |  |
| `lambda_runtime_api_host` | `""` | this is the extensions API host to register the extension with, if unset (default) then this is read from the environment variable `AWS_LAMBDA_RUNTIME_API` |  |