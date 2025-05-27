def do_not_redeem_it(function):
    """
        Custom decorator to stop execution with a message
    """
    def wrapper():
        raise SystemExit("{function.__name__} should not be called")
    return wrapper

"""
from decorators import do_not_reedem_it

@do_not_redeem_it
def get_directory_path_and_name():
"""