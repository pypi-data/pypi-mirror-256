
import functools
import pdb
import sys
import traceback
from colorama import Fore, Style


def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = traceback.extract_tb(exc_traceback)
            filename, line_number, function_name, text = traceback_details[-1]
            
            print(f"{Fore.RED}{Style.BRIGHT}Exception{Style.RESET_ALL} occurred in {Fore.YELLOW}{filename}{Style.RESET_ALL} at line {Fore.YELLOW}{line_number}{Style.RESET_ALL}")
            print(f"Function `{Fore.YELLOW}{function_name}{Style.RESET_ALL}`: \n\tline {Fore.GREEN}{text}{Style.RESET_ALL}")
            print(f"Exception type: {Fore.RED}{exc_type.__name__}{Style.RESET_ALL}")
            print(f"Exception message: {Fore.RED}{exc_value}{Style.RESET_ALL}")
            print(f"Stack trace:")
            pdb.post_mortem(exc_traceback)
    return wrapper
