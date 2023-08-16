from tests.check_files import *
import logger

def renew_logs_files():
    files = logger.LogsWriter()
    files.renew_files()


def test():
    check_files()
    renew_logs_files()
    print("TESTS PASSED")
