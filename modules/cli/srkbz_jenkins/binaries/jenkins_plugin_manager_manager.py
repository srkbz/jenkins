from os import makedirs
from os.path import join, isfile, basename

from srkbz_jenkins.logging.logger import Logger, logger
from srkbz_jenkins.paths.paths_provider import PathsProvider, paths_provider
from srkbz_jenkins.utils.download_file import download_file


class JenkinsPluginManagerManager:
    def __init__(self, logger: Logger, paths_provider: PathsProvider) -> None:
        self._logger = logger
        self._paths_provider = paths_provider

    def get_jar_file(self, version: str):
        binaries_dir = self._paths_provider.get_binaries_dir()
        return join(
            binaries_dir,
            "jenkins-plugin-manager",
            version,
            "jenkins-plugin-manager.jar",
        )

    def install(self, version: str):
        binaries_dir = self._paths_provider.get_binaries_dir()
        version_dir = join(binaries_dir, "jenkins-plugin-manager", version)
        jar_file = join(version_dir, "jenkins-plugin-manager.jar")

        if not isfile(jar_file):
            self._logger.info(f"Downloading Jenkins Plugin Manager {version}")
            makedirs(version_dir, exist_ok=True)
            jar_url = f"https://github.com/jenkinsci/plugin-installation-manager-tool/releases/download/{version}/jenkins-plugin-manager-{version}.jar"
            download_file(jar_url, jar_file, basename(jar_file))


jenkins_plugin_manager_manager = JenkinsPluginManagerManager(logger, paths_provider)
