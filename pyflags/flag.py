from pathlib import Path
from typing import Callable, Any

class flag:
    def __init__(self, canonical_name: str, value: type, type: type, validator: Callable[[Any], bool] | None = None):
        self.name = canonical_name
        self.canonical_name = canonical_name
        self.value = value
        self.type = type
        self.validator = validator

class Flags:
    def __init__(self):
        self.helpers = {} # str, str
        self.flag_values = {} # str, flag
        self.required_flags = [] # str

    def _helper_string(self, helper:str, default:type, type:type) -> str:
        return f"{helper}\nType: {type}\nDefault Value is set as: {default}"
    
    def _convert(self, value: type, target_type: type) -> type | None:
        if target_type is int:
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
        
        if target_type is Path:
            file_path = Path(value)
            if not file_path.is_file():
                raise FileNotFoundError(f"File {file_path} does not exist")
            return str(file_path)
    
        return
    
    def _get_flag_objects(self) -> dict[str, flag]:
        return self.flag_values
    
    def add(self, names: list[str], helper: str, type: type, default: type=None, required: bool=False, validator: Callable[[Any], bool] | None = None):
        canonical_name = names[0]
        shared_flag = flag(
            canonical_name=canonical_name,
            value=True if type == bool else default,
            type=type,
            validator=validator
        )

        for eachArg in names:
            self.flag_values[eachArg] = shared_flag
            self.helpers[eachArg] = self._helper_string(helper, default, type)
        
        if required:
            self.required_flags.append(canonical_name)
        pass

    def add_string(self, names:list[str], helper: str, default: str="", required: bool=False, validator: Callable[[Any], bool] | None = None):
        return self.add(names=names, helper=helper, type=str, default=default, required=required, validator=validator)
    
    def add_int(self, names:list[str], helper: str, default: int=0, required: bool=False, validator: Callable[[Any], bool] | None = None):
       return self.add(names=names, helper=helper, type=int, default=default, required=required, validator=validator)

    def add_bool(self, names:list[str], helper: str, default: bool=False, required: bool=False, validator: Callable[[Any], bool] | None = None):
       return self.add(names=names, helper=helper, type=bool, default=default, required=required, validator=validator)
    
    def add_file(self, names: list[str], helper: str, default: str = "", required: bool = False, validator: Callable[[Any], bool] | None = None):
        return self.add(names=names, helper=helper, type=Path, default=default, required=required, validator=validator)

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
            if arg in self.flag_values:
                current_flag = self.flag_values[arg]
                current_key = current_flag.canonical_name
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
                        current_flag.value = self._convert(arg, current_flag.type)
                    else:
                        current_flag.value = arg

                    # Check if there is a function to check the input
                    if current_flag.validator is not None:
                        # If the function returns negative, raise error
                        if not current_flag.validator(current_flag.value):
                            raise ValueError(f"Invalid value for {current_key}: {current_flag.value}")

                    # Reset the value
                    if current_key in self.required_flags:
                        self.required_flags.remove(current_key)

                    current_key = ""
                else:
                    raise ValueError("There is no flag for: ", arg)
        if len(self.required_flags):
            raise ValueError("Argument missing: ", ', '.join(self.required_flags))
    
    def get_flags(self) -> dict[str, str | int | bool]:
        return_dict = {}

        for key, flag in self.flag_values.items():
            if flag.value != None:
                return_dict[key] = flag.value

        return return_dict
    
    def get_value(self, key) -> str | int | bool:
        return self.flag_values[key].value

    def help_text(self):
        print("USAGE:")
        for flag, value in self.helpers.items():
            print(f"\n{flag=},{value}")