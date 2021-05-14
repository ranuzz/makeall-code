from cluedo import configuration

AppConfig = configuration.get_config()
AppConfig.setup_log()
AppConfig.setup_flask()

from cluedo.models import Sample