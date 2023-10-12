from yaml import load, Loader


def load_yml(file_path):
    """
    yml数据转化为dict数据
    :param file_path:
    :return:
    """
    with open(file_path, "rb") as f:
        return load(f, Loader=Loader)


__all__ = [
    "load_yml",
]
