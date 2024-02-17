# confygure: A simple YAML based configuration library for Python

## Install

```sh
❯ pip install confygure
```

## Usage

The library loads a `config.yml` from the current directory by default.

Given the `config.yml`:

```yaml
test: some value
```

You can use `confygure` like this:

```python
>>> from confygure import config
>>> config('test')
'some value'
```

If you want typing, you can get typed results like this:

```python
>>> from confygure import config_t, config_rt
>>> config_t(str, 'test')  # config_t ensures the return value is a str
'some value'
>>> config_t(str, 'nonexist')  # config_t allows empty values
None
>>> config_rt(str, 'nonexist')  # config_rt requires a value
KeyError: "Missing configuration key ('nonexist',)"
```

In short, you can access configuration using the following methods:

- `config(...): Any`
- `config_t(T, ...): T | None`
- `config_rt(T, ...): T`

You can use the `setup()` method to specify the location of the configuration
file and if the log level of the root logger should be configured:

Given the configuration file `example.yml`:

```yaml
test: some value

logger:
  loglevel: DEBUG
```

To load this custom configuration file and set the location of the log level
config, use something like this:

```python
>>> from confygure import setup, config
>>> setup(files=['./example.yml', '~/example.yml'],
...       logger=['logger', 'loglevel'])
>>> config()
INFO:root:Updated configuration from ./example01.yml
INFO:root:Log level set to DEBUG
{'test': 'some value', 'logger': {'loglevel': 'DEBUG'}}
```

This will actually check if a local file `./example.yml` exists and fall back
to `~/example.yml` from your home directory.
