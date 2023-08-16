import logger
import structs

class Bot:
    def __init__(self):
        pass
    
    def test_write(self):
        writer = logger.LogsWriter()

        sent = structs.SentMessage("LL", 10, "LL")
        writer.log_sent(sent)

        received = structs.ReceivedMessage("LL", 10, "DD", 11, "LL")
        writer.log_received(received)

        try:
            a = 4
            b = 554
            raise FileExistsError("FNFError")
        except FileExistsError as ex:
            exc = structs.ExceptionData(ex, a=a, b=b)
            writer.log_exception(exc)
