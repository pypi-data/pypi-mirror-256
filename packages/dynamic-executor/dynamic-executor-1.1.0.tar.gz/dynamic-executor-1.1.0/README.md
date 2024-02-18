# Dynamic-executor library for changing python code during runtime

Dynamic python is ment to be used in test development for creating and updating tests or wherever the need arises to change the code during runtime and have results visible instantaneously without restarting. The main functionality is provided by `DynamicModeExecutor().execute` generator that reloads all project-root modules (neither builtin not venv modules are reloaded).

## Documentation
Check out [documentation](https://tesla2000.github.io/dython/).

## Installation

You can install the `dynamic-executor` package using pip:

```bash
pip install dynamic-executor
```

Or by cloning the repository directly:

```bash
git clone git@github.com:Tesla2000/dynamic_executor.git
```

### Access

[Pipy](https://pypi.org/project/dynamic-executor/)

[Github](https://github.com/Tesla2000/dython)

### Usage

You can go through video tutorial to check utilities of Dynamic Executor [tutorial](https://youtu.be/RZUzBU70eKA).

```python
from dynamic_executor import DynamicModeExecutor
for error_message in DynamicModeExecutor().execute(
        locals(), globals()
    ):
    pass
```
