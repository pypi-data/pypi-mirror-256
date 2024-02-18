# These symbols must be exposed by this lib
from ._model import Model, Vtype, errors, Target, OptimizeResponse
from ._storage import S3Storage

# logger config
import logging as _logging
_logging.getLogger("TitanQ").addHandler(_logging.NullHandler())