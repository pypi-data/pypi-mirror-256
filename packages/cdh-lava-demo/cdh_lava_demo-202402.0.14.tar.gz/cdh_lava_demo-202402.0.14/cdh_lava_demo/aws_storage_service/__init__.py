"""Initialize the amzn_s3_service subpackage of cdh_lava_demo package"""

# allow absolute import from the root folder
# whatever its name is.
# from cdh_lava_demo.az_storage_service import az_storage_queue
import sys  # don't remove required for error handling
import os
from cdh_lava_demo.cdc_log_service import environment_tracing
from cdh_lava_demo.cdc_log_service import environment_logging


# Import from sibling directory ..\databricks_service
OS_NAME = os.name

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))

__all__ = ["aws_storage_file"]
