import logging

logging.basicConfig(format='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >> %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)
