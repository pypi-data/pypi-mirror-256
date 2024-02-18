import os

from bpc.log import warn


def check_both_path_exists(path: str, out_path: str):
    if not os.path.exists(path):
        raise NotImplementedError(f"{path} not exist!")

    if not os.path.exists(out_path):
        warn(f"File out path not exist! Create path like {out_path}")
        os.mkdir(out_path)
