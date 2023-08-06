from os import getcwd
from os.path import join


class PathsProvider:
    def get_config_dir(self) -> str:
        return join(getcwd(), "config")

    def get_root_dir(self) -> str:
        return join(getcwd(), ".workdir")

    def get_binaries_dir(self) -> str:
        return join(self.get_root_dir(), "binaries")

    def get_jenkins_home_dir(self) -> str:
        return join(self.get_root_dir(), "jenkins-home")


paths_provider = PathsProvider()
