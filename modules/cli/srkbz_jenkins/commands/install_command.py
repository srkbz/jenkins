from logging import Logger
from srkbz_jenkins.binaries.java_manager import JavaManager, java_manager
from srkbz_jenkins.binaries.jenkins_manager import JenkinsManager, jenkins_manager
from srkbz_jenkins.config.config_provider import ConfigProvider, config_provider


class InstallCommand:
    def __init__(
        self,
        config_provider: ConfigProvider,
        java_manager: JavaManager,
        jenkins_manager: JenkinsManager,
    ) -> None:
        self._config_provider = config_provider
        self._java_manager = java_manager
        self._jenkins_manager = jenkins_manager

    def run(self):
        config = self._config_provider.get_config()
        self._java_manager.install(config.jenkins.java_version)
        self._jenkins_manager.install(config.jenkins.version)


install_command = InstallCommand(config_provider, java_manager, jenkins_manager)
