import os

try:
    import logging

except ImportError as e:
    print('You must have logging package: logging not found')
    os.system('pip3 install logging')


logger = logging.getLogger('postgres-backup')
logger.addHandler(logging.NullHandler())
