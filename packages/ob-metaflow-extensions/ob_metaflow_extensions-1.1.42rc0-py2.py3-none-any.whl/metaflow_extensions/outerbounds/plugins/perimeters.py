import os
import fcntl
from os import path
import json


def override_metaflow_profile_with_perimeter():
    # If OBP_CONFIG_DIR is set, use that, otherwise use METAFLOW_HOME
    # If neither are set, use ~/.metaflowconfig
    obp_config_dir = path.expanduser(
        os.environ.get(
            "OBP_CONFIG_DIR", os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")
        )
    )

    file_path = os.path.join(obp_config_dir, "ob_config.json")

    if os.path.exists(file_path):
        # Acquire a shared read lock on the file
        fd = os.open(file_path, os.O_RDONLY)
        fcntl.flock(fd, fcntl.LOCK_SH)

        with open(file_path, "r") as f:
            ob_config = json.loads(f.read())

        if "OB_CURRENT_PERIMETER" in ob_config:
            os.environ["METAFLOW_PROFILE"] = ob_config["OB_CURRENT_PERIMETER"]
