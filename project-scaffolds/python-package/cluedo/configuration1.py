import os
import configparser
from pathlib import Path
import logging
from sqlalchemy import create_engine
import datetime

from cluedo import settings

# No error handling, always panic

class AppConfig:
    cluedo_home = None
    config_path = None
    instance_name = None

    # logging
    abs_log_folder = None

    base_log_folder = None
    log_file_pattern = None
    logging_level = None
    log_format = None
    simple_log_format = None

    # training
    train_dir_abs = None
    train_dir = None
    word_vec_glove_path = None


    # crawler
    crawler_output_dir_abs = None

    crawler_output_dir = None
    fuzzy_string_match_threshold = 100
    min_article_count = 1
    fresh_topic_threshold = 100

    # database
    db_engine = None

    sql_alchemy_conn = None

    # webserver
    base_url = None

    # flask
    flask_config_path = None

    def setup_log(self):
        self.abs_log_folder = os.path.join(self.cluedo_home, self.base_log_folder)
        os.makedirs(self.abs_log_folder, exist_ok=True)
        log_file = os.path.join(self.abs_log_folder, datetime.datetime.now().strftime(self.log_file_pattern) + ".log")
        logging.basicConfig(
            filename=log_file,
            filemode='w+',
            format='%(asctime)s - %(levelname)s:%(message)s',
            level=logging.DEBUG
        )

    def setup_db(self):
        self.db_engine = create_engine(self.sql_alchemy_conn)

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

def get_config():
    cluedo_home = get_cluedo_home()
    config_path = get_config_path(cluedo_home)
    config = configparser.ConfigParser()
    config.read(config_path)
    app_config = AppConfig()

    # cluedo
    app_config.cluedo_home = cluedo_home
    app_config.config_path = config_path
    app_config.instance_name = config['cluedo']['instance_name']

    # logging
    log_config = config['logging']
    app_config.log_format = log_config['log_format']
    app_config.base_log_folder = log_config['base_log_folder']
    app_config.logging_level = log_config['logging_level']
    app_config.simple_log_format = log_config['simple_log_format']
    app_config.log_file_pattern = log_config['log_file_pattern']

    # crawlers
    crawler_config = config['crawler']
    app_config.crawler_output_dir = crawler_config['crawler_output_dir']
    app_config.fuzzy_string_match_threshold = int(crawler_config['fuzzy_string_match_threshold'])
    app_config.min_article_count = int(crawler_config['min_article_count'])
    app_config.fresh_topic_threshold = int(crawler_config['fresh_topic_threshold'])

    # database
    db_config = config['database']
    app_config.sql_alchemy_conn = db_config['sql_alchemy_conn']

    # flask webserver
    web_config = config['webserver']
    app_config.base_url = web_config['base_url']

    # training
    train_config = config['training']
    app_config.train_dir = train_config['train_dir']
    app_config.word_vec_glove_path = train_config['word_vec_glove_path']

    return app_config
