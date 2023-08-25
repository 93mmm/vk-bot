from datetime import datetime


class Ex:
    def __init__(self, ex: Exception, **variables):
        self.ex: Exception = None
        self.variables: dict = None
        self.time: int = None
        
        self.ex = ex
        self.variables = variables
        self.time = datetime.now()

    def __str__(self):
        message = f"Thrown exception: {repr(self.ex)}\nVariables:\n"
        for key, value in self.variables.items():
            message += f"{key} = {value}\n"
        message += f"\nAt the time: {self.time}\n\n"
        return message + "\n"