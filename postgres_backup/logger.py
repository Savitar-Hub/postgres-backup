try:
    import logging

except ImportError:
    print('You must have logging package: logging not found')
    print('To install package: pip3 install logging')


logger = logging.getLogger('postgres-backup')
logger.addHandler(logging.NullHandler())
