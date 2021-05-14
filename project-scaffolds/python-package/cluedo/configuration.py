import os
import configparser
from pathlib import Path
import logging
import datetime

from cluedo import settings

# No error handling, always panic

class AppConfig:
    cluedo_home = None
    resource_path = None
    config_path = None
    instance_name = None

    # logging
    abs_log_folder = None

    base_log_folder = None
    log_file_pattern = None
    logging_level = None
    log_format = None
    simple_log_format = None
    cur_log_file = None

    sql_alchemy_conn = None

    # webserver
    base_url = None

    # flask
    flask_config_path = None

    def setup_log(self):
        def get_logging_level(lvl):
            if lvl == 'CRITICAL':
                return logging.CRITICAL
            elif lvl == 'ERROR':
                return logging.ERROR
            elif lvl == 'WARN':
                return logging.WARN
            elif lvl == 'INFO':
                return logging.INFO
            elif lvl == 'DEBUG':
                return logging.DEBUG
            else:
                return logging.DEBUG

        self.abs_log_folder = os.path.join(self.cluedo_home, self.base_log_folder)
        os.makedirs(self.abs_log_folder, exist_ok=True)
        log_file = os.path.join(self.abs_log_folder, datetime.datetime.now().strftime(self.log_file_pattern) + ".log")
        logging.basicConfig(
            filename=log_file,
            filemode='w+',
            format='%(asctime)s - %(levelname)s:%(message)s',
            level=get_logging_level(self.logging_level)
        )
        self.cur_log_file = log_file

    def setup_flask(self):
        self.flask_config_path = os.path.join(self.cluedo_home, 'flask_configuration.py')
        if not os.path.exists(self.flask_config_path):
            default_flask_config = _read_default_config_file('flask_configuration.py')
            with open(self.flask_config_path, 'w') as fp:
                fp.write(default_flask_config)


def _read_default_config_file(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, encoding='utf-8') as config_file:
        return config_file.read()

def get_cluedo_home():
    cluedo_home = os.getenv('CLUEDO_HOME', os.path.join(str(Path.home()), 'cluedo'))
    if not os.path.exists(cluedo_home):
        os.makedirs(cluedo_home, exist_ok=True)
    return cluedo_home

def get_config_path(cluedo_home):
    config_path = os.path.join(cluedo_home, 'cluedo.cfg')
    if not os.path.exists(config_path):
        logging.info("Creating config file in {0}".format(cluedo_home))
        default_config = _read_default_config_file('cluedo.cfg')
        with open(config_path, 'w') as fp:
            fp.write(default_config)
    if not os.path.isfile(config_path):
        raise OSError("Invalid config path {0}".format(config_path))
    return config_path

def get_resource_path(cluedo_home):
    res_path = os.path.join(cluedo_home, 'resource')
    if not os.path.exists(res_path):
        logging.info("Creating resource directory {0}".format(res_path))
        os.makedirs(res_path, exist_ok=True)
    if not os.path.isdir(res_path):
        raise OSError("Invalid resource path : {0}".format(res_path))
    if len(os.listdir(res_path)) == 0:
        logging.info("Don't forget to put data in resource folder {0}".format(res_path))
    return res_path

def get_config():
    cluedo_home = get_cluedo_home()
    config_path = get_config_path(cluedo_home)
    config = configparser.ConfigParser()
    config.read(config_path)
    app_config = AppConfig()

    # cluedo
    app_config.cluedo_home = cluedo_home
    app_config.config_path = config_path
    app_config.resource_path = get_resource_path(cluedo_home)
    app_config.instance_name = config['cluedo']['instance_name']

    # logging
    log_config = config['logging']
    app_config.log_format = log_config['log_format']
    app_config.base_log_folder = log_config['base_log_folder']
    app_config.logging_level = log_config['logging_level']
    app_config.simple_log_format = log_config['simple_log_format']
    app_config.log_file_pattern = log_config['log_file_pattern']

    # database
    db_config = config['database']
    app_config.sql_alchemy_conn = db_config['sql_alchemy_conn']

    # flask webserver
    web_config = config['webserver']
    app_config.base_url = web_config['base_url']

    return app_config
