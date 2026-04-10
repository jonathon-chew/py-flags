import os
from json import dumps
from pathlib import Path
from typing import Callable, Any

class flag:
    def __init__(
        self, 
        canonical_name: str, 
        value: str|int|bool|float|None = None, 
        value_type: type=str, 
        choices: list[str|int|bool|float] | None = None,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    )-> None: 
        self.name = canonical_name
        self.canonical_name = canonical_name
        self.value = value
        self.value_type = value_type
        self.choices = choices
        self.validator = validator
        self.custom_parse = custom_parse

class Flags:
    def __init__(self):
        self.helpers = {} # str, str
        self.flag_values = {} # str, flag
        self.required_flags = [] # str
        self.interactive_mode = False

    def _helper_string(
        self, 
        helper:str, 
        default:str|int|bool|float|None = None, 
        value_type:type=str
    ) -> str:
        return f"{helper}\nType: {value_type}\nDefault Value is set as: {default}"
    
    def _convert(self, value: str = "", target_type: str|int|bool|float|None = None) -> type | None:
        if target_type is int:
            try:
                return int(value)
            except ValueError:
                raise ValueError("Unable to convert value to int")
        
        if target_type is float:
            try:
                return float(value)
            except ValueError:
                raise ValueError("Unable to convert value to float")

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
    
    def _parse_value(self, raw: str, flag) -> Any:
        if flag.custom_parse:
            return flag.custom_parse(raw)
        return self._convert(raw, flag.value_type)
    
    def _set_flag_value(self, current_flag: flag, value: Any, current_key) -> None:
         # Check if there is a function to check the input
        if current_flag.validator is not None:
            # If the function returns negative, raise error
            if not current_flag.validator(value):
                raise ValueError(f"Invalid value for {current_key}: {value}")
            
        if current_flag.choices is not None:
            if value not in current_flag.choices:
                raise ValueError(f"{value} is not one of the possible choices {current_flag.choices}")
            pass

        if current_key in self.required_flags:
            self.required_flags.remove(current_key)
        
        current_flag.value = value
    
    def add(
            self, 
            names: list[str], 
            helper: str, 
            value_type: type, 
            default: str|int|bool|float|None = None, 
            required: bool=False, 
            choices: list[Any] | None = None,
            validator: Callable[[Any], bool] | None = None,
            custom_parse: Callable[[Any], Any] | None = None,
        ) -> None:
        canonical_name = names[0]
        shared_flag = flag(
            canonical_name=canonical_name,
            value=default,
            value_type=value_type,
            choices=choices,
            validator=validator,
            custom_parse=custom_parse
        )

        for eachArg in names:
            self.flag_values[eachArg] = shared_flag
            self.helpers[eachArg] = self._helper_string(helper, default, value_type)
        
        if required and canonical_name not in self.required_flags:
            self.required_flags.append(canonical_name)
        pass

    def add_string(
        self, 
        names:list[str], 
        helper: str, 
        default: str="", 
        required: bool=False,
        choices: list[str] | None = None,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
        return self.add(names=names, helper=helper, value_type=str, default=default, required=required, choices=choices, validator=validator, custom_parse=custom_parse)
    
    def add_int(
        self, 
        names:list[str], 
        helper: str, 
        default: int=0, 
        required: bool=False,
        choices: list[int] | None = None,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
       return self.add(names=names, helper=helper, value_type=int, default=default, required=required, choices=choices, validator=validator, custom_parse=custom_parse)

    def add_bool(
        self, 
        names:list[str], 
        helper: str, 
        default: bool=False, 
        required: bool=False,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
       return self.add(names=names, helper=helper, value_type=bool, default=default, required=required, validator=validator, custom_parse=custom_parse)
    
    def add_file(
        self, 
        names: list[str], 
        helper: str, 
        default: str = "", 
        required: bool = False,
        choices: list[str] | None = None,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
        return self.add(names=names, helper=helper, value_type=Path, default=default, required=required, choices=choices, validator=validator, custom_parse=custom_parse)
    
    def add_float(
        self, 
        names: list[str], 
        helper: str, 
        default: float = 0.0, 
        required: bool = False,
        choices: list[float] | None = None,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
        return self.add(names=names, helper=helper, value_type=float, default=default, required=required, choices=choices, validator=validator, custom_parse=custom_parse)

    def check_flag(self, argument: str) -> bool:
        return argument in self.flag_values.keys()

    def parse(self, parse_arguments: list[str]) -> None:
        current_key = ""
        missing = set(self.required_flags)
        # Check all arguments
        for arg in parse_arguments:
            if "=" in arg:
                key, value = arg.split("=", 1)
            # If this is a known flag switch to it
            if arg in self.flag_values:
                current_flag = self.flag_values[arg]
                current_key = current_flag.canonical_name
                # If it's boolean deal with it now and turn it to True
                if self.flag_values[current_key].value_type == bool:
                    # Get the flag
                    current_flag = self.flag_values[current_key]
                    # Set the value
                    current_flag.value = True
                    # Reset the value
                    self.flag_values[current_key] = current_flag
                    current_flag, current_key = "", ""

                    if current_key in missing:
                        missing.remove(arg)
            else:
                if current_key != "":
                    current_flag = self.flag_values[current_key]
                    parseed_value = self._parse_value(arg, current_flag)

                    self._set_flag_value(current_flag, parseed_value, current_key)

                    current_key = ""
                else:
                    raise ValueError(f"There is no flag for: {arg}")
                
        if len(missing):
            if not self.interactive_mode:
                raise ValueError(f"Argument missing: {', '.join(missing)}")
            else:
                for missing_flag in missing:
                    print(f"{missing_flag} ({self.flag_values[missing_flag].value_type.__name__}) is required.")
                    print(f"{self.helpers[missing_flag]}")
                    info = input()
                    parseed_value = self._parse_value(info, self.flag_values[missing_flag])
                    self._set_flag_value(self.flag_values[missing_flag], parseed_value, missing_flag)
    
    def get_flags(self) -> dict[str, str | int | bool]:
        return_dict = {}

        for key, flag in self.flag_values.items():
            if flag.value is not None:
                return_dict[key] = flag.value
        return return_dict
    
    def debug_flags(self) -> str:
        return dumps(self.get_flags())
    
    def activate_interactive_mode(self) -> None:
        self.interactive_mode = True
    
    def get_value(self, key: str) -> str | int | bool:
        return self.flag_values[key].value

    def help_text(self) -> None:
        print("USAGE:")
        for flag, value in self.helpers.items():
            print(f"\n{flag=},{value}")