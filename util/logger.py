import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >> %(message)s')

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

log.addHandler(streamHandler)
