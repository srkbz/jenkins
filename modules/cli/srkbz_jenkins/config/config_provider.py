from os.path import join
import tomli
from srkbz_jenkins.config.model import Config
from srkbz_jenkins.paths.paths_provider import PathsProvider, paths_provider


class ConfigProvider:
    def __init__(self, paths_provider: PathsProvider) -> None:
        self._paths_provider = paths_provider

    def get_config(self) -> Config:
        config_file_path = join(self._paths_provider.get_config_dir(), "config.toml")
        with open(config_file_path, "rb") as f:
            toml_dict = tomli.load(f)
        return Config(**toml_dict)


config_provider = ConfigProvider(paths_provider)
