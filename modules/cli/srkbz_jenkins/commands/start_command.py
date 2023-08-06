from subprocess import run
from os.path import join
from os import environ

from srkbz_jenkins.binaries.java_manager import JavaManager, java_manager
from srkbz_jenkins.binaries.jenkins_manager import JenkinsManager, jenkins_manager
from srkbz_jenkins.config.config_provider import ConfigProvider, config_provider
from srkbz_jenkins.paths.paths_provider import PathsProvider, paths_provider


class StartCommand:
    def __init__(
        self,
        paths_provider: PathsProvider,
        config_provider: ConfigProvider,
        java_manager: JavaManager,
        jenkins_manager: JenkinsManager,
    ) -> None:
        self._paths_provider = paths_provider
        self._config_provider = config_provider
        self._java_manager = java_manager
        self._jenkins_manager = jenkins_manager

    def run(self):
        config = self._config_provider.get_config()
        java_home = self._java_manager.get_home_dir(config.jenkins.java_version)
        jenkins_war = self._jenkins_manager.get_war_file(config.jenkins.version)

        run(
            [join(java_home, "bin", "java"), "-jar", jenkins_war],
            env=dict(
                environ,
                JENKINS_HOME=join(self._paths_provider.get_jenkins_home_dir()),
                CASC_JENKINS_CONFIG=join(
                    self._paths_provider.get_config_dir(), "jcasc.yaml"
                ),
            ),
        )


start_command = StartCommand(
    paths_provider, config_provider, java_manager, jenkins_manager
)
