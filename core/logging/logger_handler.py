import logging
import logging.config
import yaml

with open("./core/logging/middleware_log_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
