import custom_logs
import msg

class Bot:
    def __init__(self):
        pass
    
    def test_write(self):
        writer = custom_logs.LogsWriter()

        sent = msg.SentMessage("LL", 10, "LL")
        writer.log_sent(sent)

        received = msg.ReceivedMessage("LL", 10, "DD", 11, "LL")
        writer.log_received(received)

        try:
            a = 4
            b = 554
            raise FileExistsError("FNFError")
        except FileExistsError as ex:
            exc = msg.ExceptionData(ex, a=a, b=b)
            writer.log_exception(exc)