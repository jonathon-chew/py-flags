class flag:
    def __init__(self, argument: str, canonical: str, value: str | int | bool, type: str | int | bool):
        self.argument = argument
        self.canonical = canonical
        self.value = value
        self.type = type

class argument:
    def __init__(self):
        self.helpers = {}
        self.flag_values = {} # str, flag
        self.required_flags = []

    def __helper_string__(self, helper, default):
        return f"Useage: {helper}\nType: string\nDefault Value is set as: {default}"

    def add_string(self, arguments:list[str], helper: str, default: str="", required: bool=False):
        # print(f"Adding: {arguments=}, {helper=}, {default=}")
        canonical_name=arguments[0]
        shared_flag = flag(
            argument=canonical_name, 
            canonical=canonical_name, 
            value=default, 
            type=str
        )
        for eachArg in arguments:
            self.flag_values[eachArg] = shared_flag
            self.helpers[eachArg] = self.__helper_string__(helper, default)
        if required:
            self.required_flags.append(canonical_name)
    
    def add_int(self, arguments:list[str], helper: str, default: int=0, required: bool=False):
        # print(f"Adding: {arguments=}, {helper=}, {default=}")
        canonical_name = arguments[0]
        shared_flag = flag(
            argument=canonical_name, 
            canonical=canonical_name, 
            value=default, 
            type=int
        )
        for eachArg in arguments:
            self.flag_values[eachArg] = shared_flag
            self.helpers[eachArg] = self.__helper_string__(helper, default)
        if required:
            self.required_flags.append(canonical_name)

    def add_bool(self, arguments:list[str], helper: str, default: bool=False, required: bool=False):
        # print(f"Adding: {arguments=}, {helper=}, {default=}")
        canonical_name = arguments[0]
        shared_flag = flag(
            argument=canonical_name, 
            canonical=canonical_name, 
            value=default, 
            type=bool
        )
        for eachArg in arguments:
            self.flag_values[eachArg] = shared_flag
            self.helpers[eachArg] = self.__helper_string__(helper, default)
        if required:
            self.required_flags.append(canonical_name)

    def check_flag(self, argument) -> bool:
        for arg in self.flag_values.keys():
            if arg == argument:
                return True
        else:
            return False

    def __convert__(self, value: int | bool, target_type: type) -> int | bool | str:
        if target_type is target_type is int:
            try:
                return int(value)
            except ValueError:
                raise ValueError("Unable to convert value to int")

        if target_type is bool:
            lowered = value.lower()
            if lowered in ("true", "1", "yes", "on"):
                return True
            if lowered in ("false", "0", "no", "off"):
                return False
            raise ValueError("Unable to convert value to bool")

        if target_type is str:
            return value

    def parse(self, parse_arguments: list[str]):
        current_key = ""
        # Check all arguments
        for arg in parse_arguments:
            # If this is a known flag switch to it
            if arg in self.flag_values:
                current_flag = self.flag_values[arg]
                current_key = current_flag.canonical
                # If it's boolean deal with it now and turn it to True
                if self.flag_values[current_key].type == bool:
                    # Get the flag
                    current_flag = self.flag_values[current_key]
                    # Set the value
                    current_flag.value = True
                    # Reset the value
                    self.flag_values[current_key] = current_flag
                    current_flag, current_key = "", ""

                    if arg in self.required_flags:
                        self.required_flags.remove(arg)
            else:
                if current_key != "":
                   # Get the flag
                    current_flag = self.flag_values[current_key]

                    # Set the value
                    if current_flag.type != str:
                        current_flag.value = self.__convert__(arg, current_flag.type)
                    else:
                        current_flag.value = arg
                    # Reset the value
                    if current_key in self.required_flags:
                        self.required_flags.remove(current_key)

                    current_key = ""
                else:
                    raise NameError("There is no flag for: ", arg)
        if len(self.required_flags):
            raise ValueError("Argument missing: ", ', '.join(self.required_flags))
    
    def get_flags(self) -> dict[str, flag]:
        return self.flag_values
    
    def get_value(self, key) -> str | int | bool:
        return self.flag_values[key].value

    def helper(self):
        print("USEAGE:")
        for key, value in self.helpers.items():
            print(f"{key=}, {value=}")