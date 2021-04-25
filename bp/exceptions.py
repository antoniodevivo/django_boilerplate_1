from rest_framework.views import exception_handler
import logging, sys, traceback

logger = logging.getLogger("textlogger")

def generic_exception_handler(exc, context, *args):
    response = exception_handler(exc, context)
    traceback.print_exc(file=sys.stdout)
    logger.info(traceback.format_exc())
    return response

def manual_string_logger(message):
    logger.info(str(message))
