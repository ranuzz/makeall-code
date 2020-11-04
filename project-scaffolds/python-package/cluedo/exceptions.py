import logging

class CluedoInitException(Exception):
    
    def __init__(self):
        logging.error("Cluedo Initialization error")