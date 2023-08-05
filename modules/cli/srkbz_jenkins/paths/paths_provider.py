from os import getcwd
from os.path import join


class PathsProvider:
    def get_config_dir(self) -> str:
        return join(getcwd(), "config")

    def get_binaries_dir(self) -> str:
        return join(getcwd(), ".workdir", "binaries")


paths_provider = PathsProvider()
