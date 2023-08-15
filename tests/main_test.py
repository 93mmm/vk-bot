from tests.check_files import *
import custom_logs

def renew_logs_files():
    files = custom_logs.LogsWriter()
    files.renew_files()


def test():
    check_files()
    renew_logs_files()
    print("TESTS PASSED")
