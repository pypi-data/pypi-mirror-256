import ipih

from build_tools import build
from MobileHelperService.const import SD

build(SD, additional_modules=["pih-mio-content", "pillow", "numpy"])