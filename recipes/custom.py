# -*- Mode: Python -*- vi:si:et:sw=4:sts=4:ts=4:syntax=python
import os
import shutil
from collections import defaultdict

from cerbero.build import recipe
from cerbero.build.source import SourceType
from cerbero.build.cookbook import CookBook
from cerbero.config import Platform
from cerbero.enums import License
from cerbero.utils import shell, to_unixpath

class Ribbon:

    version = '0.9.0'
    commit = '0.9'

