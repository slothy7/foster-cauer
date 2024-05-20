"""parsing"""

import argparse
import sys
from typing import NoReturn


class MyParser(argparse.ArgumentParser):
    """Custom argparse class for better error handling"""

    def error(self, message: str) -> NoReturn:
        sys.stderr.write(f"!!!!\nERROR: {message}\n!!!!\n")
        self.print_help(sys.stderr)
        sys.exit(2)
