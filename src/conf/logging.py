LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(processName)s[%(process)d] %(name)s %(levelname)s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },

    },
    'loggers': {
        # silence the noisy ones
    },
    'root': {
        'handlers': [
            'console',
        ],
        'level': 'DEBUG',  # emit DEBUG and above
        'propagate': False,
    },
}
