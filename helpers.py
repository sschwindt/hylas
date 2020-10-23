from config import *


def cache(fun):
    """Makes a function running in a ``__cache__`` sub-folder to enable deleting temporary trash files."""
    def wrapper(*args, **kwargs):
        check_cache()
        fun(*args, **kwargs)
        remove_directory(cache_folder)
    return wrapper


def check_cache():
    """Creates the cache folder if it does not exist."""
    try:
        os.makedirs(cache_folder)
    except OSError:
        pass


def dict2str(dictionary, **kwargs):
    """Converts a dict to a string expression.

    Args:
        dictionary (dict): A dictionary to convert to a string.

    Keyword Args:
        inverse_dict(boolean): Apply inverse order of string (default: ``False``).

    Returns:
        str: The dictionary as flattened text.

    Example:
        ``>>> dict2str({e: 1, f: 2, ...})``
        ``Out[]: "{e: 1, f: 2, ...}"``
    """

    if kwargs.get("inverse_dict"):
        inverse_dict = kwargs.get("inverse_dict")
    else:
        inverse_dict = False  # optional keyword arg: if true: dictionary keys and values will be inversed

    dict_str = "{"
    cc = 1
    for k, v in dictionary.items():
        skey = "\'%s\'" % k if type(k) == str else str(k)
        sval = "\'%s\'" % v if type(v) == str else str(v)
        if not inverse_dict:
            dict_str += "{0}: {1}".format(skey, sval)
        else:
            dict_str += "{1}: {0}".format(skey, sval)
        if not (cc == dictionary.__len__()):
            dict_str += ", "
        else:
            dict_str += "}"
        cc += 1
    return dict_str


def log_actions(fun):
    """Wraps a function with a logger. All actions of the wrapped function can be writting to ``ROOT/logfile.log``."""
    def wrapper(*args, **kwargs):
        start_logging()
        fun(*args, **kwargs)
        logging.shutdown()
    return wrapper


def remove_directory(directory):
    """Removes a directory and all its contents - be careful!

    Args:
        directory (str): directory to remove (delete)

    Returns:
        None: Deletes directory.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        shutil.rmtree(directory)
    except PermissionError:
        print("WARNING: Could not remove %s (files locked by other program)." % directory)
    except FileNotFoundError:
        print("WARNING: The directory %s does not exist." % directory)
    except NotADirectoryError:
        print("WARNING: %s is not a directory." % directory)


def start_logging():
    """Creates a log file (``ROOT/logfile.log``)."""
    logging.basicConfig(filename="logfile.log", format="[%(asctime)s] %(message)s",
                        filemode="w", level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
