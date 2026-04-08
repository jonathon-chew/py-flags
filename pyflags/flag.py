class flag:
    def __init__(self, argument, value, type):
        self.argument = argument
        self.value = value
        self.type = type

class argument:
    def __init__(self):
        self.helpers = {}
        self.flag_values = {} # str, flag

    def add_string(self, arguments:list[str], helper: str, default: str=""):
        print(f"Adding: {arguments=}, {helper=}, {default=}")
        for eachArg in arguments:
            self.flag_values[eachArg] = flag(argument=eachArg, value=default, type=str)
            self.helpers[eachArg] = helper
    
    def add_int(self, arguments:list[str], helper: str, default: int=0):
        print(f"Adding: {arguments=}, {helper=}, {default=}")
        for eachArg in arguments:
            self.flag_values[eachArg] = flag(argument=eachArg, value=default, type=int)
            self.helpers[eachArg] = helper

    def add_bool(self, arguments:list[str], helper: str, default: bool=False):
        print(f"Adding: {arguments=}, {helper=}, {default=}")
        for eachArg in arguments:
            self.flag_values[eachArg] = flag(argument=eachArg, value=default, type=bool)
            self.helpers[eachArg] = helper

    def check_flag(self, argument) -> bool:
        for arg in self.flag_values.keys():
            if arg == argument:
                return True
        else:
            return False

    def parse(self, parse_arguments: list[str]):
        current_key = ""
        # Check all arguments
        for arg in parse_arguments:
            # If this is a known flag switch to it
            if arg in self.flag_values.keys():
                current_key = arg
                # If it's boolean deal with it now and turn it to True
                if self.flag_values[current_key].type == bool:
                    # Get the flag
                    current_flag = self.flag_values[current_key]
                    # Set the value
                    current_flag.value = True
                    # Reset the value
                    self.flag_values[current_key] = current_flag
                    current_flag, current_key = "", ""
            else:
                if current_key != "":
                   # Get the flag
                    current_flag = self.flag_values[current_key]
                    # Set the value
                    current_flag.value = arg
                    # Reset the value
                    self.flag_values[current_key] = current_flag
                    current_flag, current_key = "", ""
    
    def get_flags(self) -> dict[str, flag]:
        return self.flag_values

    def helper(self):
        print("USEAGE:")
        for key, value in self.helpers.items():
            print(f"{key=}, {value=}")

