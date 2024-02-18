from dcre._version import get_versions

from .erfani_2022 import figures

versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
from . import _version

__version__ = _version.get_versions()["version"]
