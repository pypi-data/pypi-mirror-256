import logging
import sys

log = logging.getLogger('GWSS')

sout_handler = logging.StreamHandler(sys.stdout)
sout_handler.setLevel(logging.DEBUG)

sout_formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
sout_handler.setFormatter(sout_formatter)
log.addHandler(sout_handler)
logger = log
