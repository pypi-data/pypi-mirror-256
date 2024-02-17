"""Initialize the tests unit test subpackage of cdh_lava_core package"""

import sys
import os

OS_NAME = os.name

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("tests: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("tests: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))


__all__ = [
    filename[:-3]
    for filename in os.listdir(os.path.dirname(__file__))
    if filename.startswith("test_")
]
