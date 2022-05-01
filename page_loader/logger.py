
logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'std_format': {
            'format': '{filename}::{funcName}::{levelname}::{name}: {message}',
            'style': '{'
        }
    },
    'handlers': {
        'ch': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format'
        }
    },
    'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['ch']
            # 'propagate': False
        }
    }
}
