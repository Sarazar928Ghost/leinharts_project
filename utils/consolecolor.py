class ConsoleColor:
    bcolors = {
        "HEADER": '\033[95m',
        "OKBLUE": '\033[94m',
        "OKCYAN": '\033[96m',
        "OKGREEN": '\033[92m',
        "WARNING": '\033[93m',
        "FAIL": '\033[91m',
        "ENDC": '\033[0m',
        "BOLD": '\033[1m',
        "UNDERLINE": '\033[4m'
    }

    @staticmethod
    def print_fail(message) -> None:
        print(f"{ConsoleColor.bcolors['FAIL']}{message}{ConsoleColor.bcolors['ENDC']}")

    @staticmethod
    def print_warning(message) -> None:
        print(f"{ConsoleColor.bcolors['WARNING']}{message}{ConsoleColor.bcolors['ENDC']}")

    @staticmethod
    def print_success(message) -> None:
        print(f"{ConsoleColor.bcolors['OKGREEN']}{message}{ConsoleColor.bcolors['ENDC']}")
