from os import makedirs
from os.path import join, isfile, basename

from srkbz_jenkins.logging.logger import Logger, logger
from srkbz_jenkins.paths.paths_provider import PathsProvider, paths_provider
from srkbz_jenkins.utils.download_file import download_file


class JenkinsManager:
    def __init__(self, logger: Logger, paths_provider: PathsProvider) -> None:
        self._logger = logger
        self._paths_provider = paths_provider

    def install(self, version: str):
        binaries_dir = self._paths_provider.get_binaries_dir()
        version_dir = join(binaries_dir, "jenkins", version)
        jenkins_file = join(version_dir, "jenkins.war")

        if not isfile(jenkins_file):
            self._logger.info(f"Downloading Jenkins {version}")
            makedirs(version_dir, exist_ok=True)
            version_url = f"https://github.com/jenkinsci/jenkins/releases/download/jenkins-{version}/jenkins.war"
            download_file(version_url, jenkins_file, basename(jenkins_file))


jenkins_manager = JenkinsManager(logger, paths_provider)
# https://github.com/jenkinsci/plugin-installation-manager-tool
