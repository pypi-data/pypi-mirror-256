import ipih

from pih_tls import NAME, VERSION
from build_tools import build

build(
    NAME,
    "Shared tools for PIH module",
    VERSION,
    None,
    [
        "pillow",
        "numpy",
        "pdf2image",
    ],
    install_default_module = False
)