from json import dumps
from pathlib import Path
from typing import Callable, Any, get_origin, get_args

class flag:
    def __init__(
        self, 
        canonical_name: str, 
        value: Any|None = None, 
        value_type: type=str, 
        choices: list[Any] | None = None,
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

    def __getattr__(self, name) -> Any:
        try:
            if name in self.flag_values.keys():
                return self.flag_values[name].value
            
            check_me = {self._normalize(k): v for k, v in self.flag_values.items()}
            return check_me[name].value
            
        except:
             raise AttributeError(f"No such attribute: {name}")


    def _normalize(self, name: str) -> str:
        return name.lstrip("-").replace("-", "_")

    def _helper_string(
        self, 
        helper:str, 
        default:Any|None = None, 
        value_type:type=str
    ) -> str:
        """
        Create the helper message to be passed back to the user to try and guide them what is missing and what this will need to be
        """
        return f"{helper}\nType: {value_type}\nDefault Value is set as: {default}"
    
    def _convert(self, value: str = "", target_type: Any|None = None) -> Any | None:
        """
        Handling type conversion for supported input typess
        """
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
        """
        Internal function for ascertaining whether to use the supported internal logic to convert the type to the right value OR the passed in function
        """
        inner_type = self._get_list_inner_type(flag.value_type)

        if inner_type is not None:
            return self._convert(raw, inner_type)
        
        if flag.custom_parse:
            return flag.custom_parse(raw)
        return self._convert(raw, flag.value_type)
    
    def _set_flag_value(self, current_flag: flag, value: Any, current_key) -> None:
        """
        Refactored logic from the parser so this can be called for missing flags and at other points
        """
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
        
        inner_type = self._get_list_inner_type(current_flag.value_type)

        if inner_type is not None:
            if current_flag.value is None:
                current_flag.value = []
            current_flag.value.append(value)
        else:
            current_flag.value = value
    
    def _add_missing_key(self, key: str) -> None:
        """
        Internal function for asking the user for input!
        """
        print(f"{key} ({self.flag_values[key].value_type.__name__}) is required.")
        print(f"{self.helpers[key]}")
        info = input()
        parseed_value = self._parse_value(info, self.flag_values[key])
        self._set_flag_value(self.flag_values[key], parseed_value, key)
    

    def _get_list_inner_type(self, value_type):
        origin = get_origin(value_type)

        # Case 1: list[str], list[int], etc.
        if origin is list:
            return get_args(value_type)[0]

        # Case 2: plain list → default to str
        if value_type == list:
            return str

        return None
    
    def add(
            self, 
            names: list[str], 
            helper: str, 
            value_type: Any, 
            default: Any|None = None, 
            required: bool=False, 
            choices: list[Any] | None = None,
            validator: Callable[[Any], bool] | None = None,
            custom_parse: Callable[[Any], Any] | None = None,
        ) -> None:
        """
        The basis of the logic - make a flag and all it's aliases and set all the values
        """
        canonical_name = names[0]
        inner_type = self._get_list_inner_type(value_type)
        shared_flag = flag(
            canonical_name=canonical_name,
            value=[] if inner_type is not None else default,
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

    def add_string(
        self, 
        names:list[str], 
        helper: str, 
        default: str | None = None,
        required: bool=False,
        choices: list[str] | None = None,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
        """
        Concise calling - this only needs a name / names and a helper string to call to make a flag which has a value of a string
        """
        return self.add(names=names, helper=helper, value_type=str, default=default, required=required, choices=choices, validator=validator, custom_parse=custom_parse)
    
    def add_int(
        self, 
        names:list[str], 
        helper: str, 
        default: int | None = None,
        required: bool=False,
        choices: list[int] | None = None,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
        """
        Concise calling - this only needs a name / names and a helper string to call to make a flag which has a value of a int
        """
        return self.add(names=names, helper=helper, value_type=int, default=default, required=required, choices=choices, validator=validator, custom_parse=custom_parse)

    def add_bool(
        self, 
        names:list[str], 
        helper: str, 
        default: bool,
        required: bool=False,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
        """
        Concise calling - this only needs a name / names and a helper string to call to make a flag which has a value of a boolean
        All booleans are false by default, users declare the flag to turn it to true (unless otherwise specified)
        """
        return self.add(names=names, helper=helper, value_type=bool, default=default, required=required, validator=validator, custom_parse=custom_parse)
    
    def add_file(
        self, 
        names: list[str], 
        helper: str, 
        default: str | None = None,
        required: bool = False,
        choices: list[str] | None = None,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
        """
        Concise calling - this only needs a name / names and a helper string to call to make a flag which has a value of a string
        This confirms the path of the file is valid and not malformed/missing in anyway
        """
        return self.add(names=names, helper=helper, value_type=Path, default=default, required=required, choices=choices, validator=validator, custom_parse=custom_parse)
    
    def add_float(
        self, 
        names: list[str], 
        helper: str, 
        default: float | None = None,
        required: bool = False,
        choices: list[float] | None = None,
        validator: Callable[[Any], bool] | None = None,
        custom_parse: Callable[[Any], Any] | None = None
    ) -> None:
        """
        Concise calling - this only needs a name / names and a helper string to call to make a flag which has a value of a float
        """
        return self.add(names=names, helper=helper, value_type=float, default=default, required=required, choices=choices, validator=validator, custom_parse=custom_parse)

    def check_flag(self, argument: str) -> bool:
        return argument in self.flag_values.keys()

    def parse(self, parse_arguments: list[str]) -> None:
        """
        Parsed what has been passed in -> if it's a flag or value based upon what has been stored
        """
        current_key = ""
        missing = set(self.required_flags)
        # Check all arguments
        for arg in parse_arguments:
            if "=" in arg:
                key, value = arg.split("=", 1)
                if key in self.flag_values:
                    current_flag = self.flag_values[key]
                    current_key = current_flag.canonical_name
                    parsed_value = self._parse_value(value, current_flag)
                    self._set_flag_value(current_flag, parsed_value, current_key)
                    current_key = ""
                    continue
                raise ValueError(f"There is no flag for: {key}")
            # If this is a known flag switch to it
            if arg in self.flag_values:
                current_flag = self.flag_values[arg]
                current_key = current_flag.canonical_name
                # If it's boolean deal with it now and turn it to True
                if self.flag_values[current_key].value_type == bool:
                    current_flag.value = True

                    if current_key in missing:
                        missing.remove(current_key)
                    current_key = ""
                    continue
            else:
                if current_key:
                    current_flag = self.flag_values[current_key]
                else:
                    raise ValueError(f"There is no flag for: {arg}")
                
                if current_flag.value_type == bool:
                    parsed_value = self._convert(arg, current_flag.value_type)
                else:
                    parsed_value = self._parse_value(arg, current_flag)

                self._set_flag_value(current_flag, parsed_value, current_key)

                if self._get_list_inner_type(current_flag.value_type) is None:
                    current_key = ""
                
    def parse_and_resolve(self, parse_arguments: list[str]) -> None:
        self.activate_interactive_mode()
        self.parse(parse_arguments)
        self.resolve_all()
    
    def resolve_all(self):
        """
        Force all required flags to be handled when ever you want in your script
        """
        missing = list(self.required_flags)
        if len(missing):
            if not self.interactive_mode:
                raise ValueError(f"Argument missing: {', '.join(missing)}")
            else:
                _ = [self._add_missing_key(missing_flag) for missing_flag in missing if self.flag_values[missing_flag].value is None]
    
    def get_flags(self) -> dict[str, str | int | bool | float | list]:
        """
        Useful for debuging, showing currently set states of all passed in flags
        """
        return_dict = {key: flag.value for key, flag in self.flag_values.items() if flag.value is not None or flag.value != []}
        return return_dict
    
    def has_value(self, key: str) -> bool :
        """
        Simple debuging for calling a specific flag and confirming whether or not the flag was provided
        """
        return self.flag_values[key].value is not None
    
    def resolve(self, key:str) -> Any:  
        """
        Call this function if you want the user to be prompted if the flag is not set, so the script / flow doesn't break
        
        eg. if flags.get_value("--save"):
                file = flags.resolve("--output-file")
        
        If they forget to set an output file this will ask!

        This is intended to be safe and interactive
        """
        flag = self.flag_values[key]

        if flag.value is None:
            if not self.interactive_mode:
                raise ValueError(f"{key} is required but not set")

            self._add_missing_key(key)

        return flag.value
    
    def get_optional(self, key: str, default: Any) -> str | int | bool | float | list:
        """
        Call this function if you want to check if the user chose something or not, and set a default if they did not
        
        eg. if flags.get_value("--output", "./results.json"): ...
        
        If the user has set the flag, it will return the flag value OR use something you define

        This is intended to be safe
        """
        flag = self.flag_values[key]
        return flag.value if flag.value is not None else default
    
    def get_value(self, key: str) -> str | int | bool | float | list:
        """
        Call this function if you don't want the user to be prompted if the flag is not set AND the value MUST be set with no fall back if not
        
        eg. if flags.get_value("--override"): ...
        
        If the user has set the flag, this will return value (assuming it's a bool flag, it' will return true)

        This is intentionally strict
        """

        if self.flag_values[key].value is not None:
            return self.flag_values[key].value
        else:
            raise ValueError(f"{key} is not set")
    
    def debug_flags(self) -> str:
        """
        Return a JSON string as to the current set up config - useful for logging
        """
        return dumps(self.get_flags())
    
    def activate_interactive_mode(self) -> None:
        """
        Helper function to configure the CLI - this means users will be prompted for required flags if missing
        Users will also be prompted at any stage get_value is called and the flag is not set BUT the flag is not required
        """
        self.interactive_mode = True
    
    def help_text(self) -> None:
        """
        Print to screen the possible options, the definied helper text, and key information
        """
        print("USAGE:")
        for flag, value in self.helpers.items():
            print(f"\n{flag=},{value}")

    def help_text_ordered(self) -> None:
        print("USAGE:")

        # Required first
        for flag in self.required_flags:
            print(f"\n{flag} (required)")
            print(self.helpers[flag])

        # Then optional
        for flag, helper in self.helpers.items():
            if flag in self.required_flags:
                continue

            print(f"\n{flag} (optional)")
            print(helper)