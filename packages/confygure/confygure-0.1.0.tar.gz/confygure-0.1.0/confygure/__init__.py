import logging
import logging.config
import os
import yaml

from typing import Optional, Type, TypeVar

T = TypeVar('T')
__config = {}
__setup_configure_logger: list[str] = []
__setup_config_files: list[str] = ['config.yml']


def setup(files: Optional[list] = None, logger: Optional[list] = None):
    '''Configure confygure.

    :param files: Tuple or list of configuration files. The first file that
                  exists will be used. Setting this to `None` will not modify
                  the default. The default is `('config.yml')`.
    :param logger: Tuple or list specifying the patch to a log level
                   configuration for the root logger.
    '''
    global __setup_config_files
    global __setup_configure_logger
    if files is not None:
        if type(files) not in (list, tuple):
            raise Exception('Configuration files must be a tuple or list')
        __setup_config_files = [os.path.expanduser(f) for f in files]
    if logger is not None:
        __setup_configure_logger = logger


def configuration_file() -> Optional[str]:
    '''Find the best match for the configuration file.  The configuration file
    locations taken into consideration can be configured using `setup()`.

    :return: configuration file name or None
    '''
    for filename in __setup_config_files:
        if os.path.isfile(filename):
            return filename


def update_configuration(filename: Optional[str] = None):
    '''Update configuration from file.
    If no filename is specified, the best match from the files configured via
    `setup()` is being used.
    '''
    cfgfile = filename or configuration_file()
    if not cfgfile:
        return {}
    with open(cfgfile, 'r') as f:
        cfg = yaml.safe_load(f)
    globals()['__config'] = cfg

    # update logger
    logger_config = __setup_configure_logger
    if logger_config:
        loglevel = (config_t(str, *logger_config) or 'INFO').upper()
        logging.root.setLevel(loglevel)
        logging.info('Updated configuration from %s', cfgfile)
        logging.info('Log level set to %s', loglevel)
    return cfg


def config(*args):
    '''Get a specific configuration value.
    This will load the configuration file if necessary.

    :return: The configuration value
    '''
    cfg = __config or update_configuration()
    for key in args:
        if cfg is None:
            return
        cfg = cfg.get(key)
    return cfg


def config_t(type_: Type[T], *args: str) -> Optional[T]:
    '''Get a specific configuration value or the whole configuration.
    The value type is checked against the provided type.
    A None value is allowed.
    A TypeError is raised if the check fails.
    This will load the configuration file if necessary.

    Note: This will only work for simple types like `int` or `str`.
    Complex type specifications like `dict[str, int]` will not work.

    :param type_: The type to check for
    :return: Configuration value
    :raises: TypeError if configuration value does not match
    '''
    if type_ and not isinstance(type_, type):
        raise TypeError('verify_type must by a type')
    cfg = config(*args)
    if cfg is not None and not isinstance(cfg, type_):
        raise TypeError(f'Value has unexpected type {type(cfg)}')
    return cfg


def config_rt(type_: Type[T], *args: str) -> T:
    '''Get a specific configuration value or the whole configuration.
    The value type is checked against the provided type.
    A TypeError is raised if the check fails.
    The configuration value is required. A None value will raise a KeyError.
    This will load the configuration file if necessary.

    Note: This will only work for simple types like `int` or `str`.
    Complex type specifications like `dict[str, int]` will not work.

    :param type_: The type to check for
    :return: Configuration value
    :raises: TypeError if configuration value does not match
    :raises: KeyError if the requested configuration value does not exist
    '''
    cfg = config_t(type_, *args)
    if cfg is None:
        raise KeyError(f'Missing configuration key {args}')
    return cfg
