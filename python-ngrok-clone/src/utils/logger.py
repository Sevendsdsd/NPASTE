import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger with a specified name and log file."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console_handler)
    
    return logger

# Example usage
# logger = setup_logger('ngrok_clone', 'ngrok_clone.log')
# logger.info('Logger is set up and ready to use.')