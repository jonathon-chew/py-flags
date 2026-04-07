class argument:
    def __init__(self):
        self.flags = []
        self.helpers = {}

    def add_string(self, arguments:list[str], helper: str, default: str=""):
        print(f"Adding: {arguments=}, {helper=}, {default=}")
        for eachArg in arguments:
            self.flags.append(eachArg)
            self.helpers[eachArg] = helper

    def check_flag(self, argument) -> bool:
        for arg in self.flags:
            if arg == argument:
                return True
        else:
            return False

    def helper(self):
        print("USEAGE:")
        for key, value in self.helpers.items():
            print(f"{key=}, {value=}")

