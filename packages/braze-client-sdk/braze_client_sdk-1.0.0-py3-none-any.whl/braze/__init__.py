# -*- coding: utf-8 -*-

__all__ = ["Braze"]

import sys
from pathlib import Path

PACKAGE_PATH = Path(__file__).parent
sys.path.append(str(PACKAGE_PATH))

from .sdk import Braze

__version__ = "1.0.0"