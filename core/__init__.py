import yaml
import logging
import logging.config
from decouple import config

with open(config("CORE_LOG_CONFIG"), "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

# Now, any module where __name__ starts with `my_app` will use the config.
logger = logging.getLogger(__name__)