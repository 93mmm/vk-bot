from datetime import datetime
from traceback import format_exc


class Ex:
    def __init__(self, **variables):
        self.variables: dict = None
        self.time: int = None
        
        self.variables = variables
        self.time = datetime.now()

    def __str__(self):
        message = f"{format_exc()}\nVariables:\n"
        for key, value in self.variables.items():
            message += f"{key} = {value}\n"
        message += f"\nAt the time: {self.time}\n\n"
        return message + "\n"
