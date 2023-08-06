from subprocess import run
from os.path import join
from os import environ

from srkbz_jenkins.binaries.java_manager import JavaManager, java_manager
from srkbz_jenkins.binaries.jenkins_manager import JenkinsManager, jenkins_manager
from srkbz_jenkins.binaries.jenkins_plugin_manager_manager import (
    JenkinsPluginManagerManager,
    jenkins_plugin_manager_manager,
)
from srkbz_jenkins.config.config_provider import ConfigProvider, config_provider
from srkbz_jenkins.paths.paths_provider import PathsProvider, paths_provider


class InstallCommand:
    def __init__(
        self,
        paths_provider: PathsProvider,
        config_provider: ConfigProvider,
        java_manager: JavaManager,
        jenkins_manager: JenkinsManager,
        jenkins_plugin_manager_manager: JenkinsPluginManagerManager,
    ) -> None:
        self._paths_provider = paths_provider
        self._config_provider = config_provider
        self._java_manager = java_manager
        self._jenkins_manager = jenkins_manager
        self._jenkins_plugin_manager_manager = jenkins_plugin_manager_manager

    def run(self):
        config = self._config_provider.get_config()

        self._java_manager.install(config.jenkins.java_version)
        self._jenkins_manager.install(config.jenkins.version)
        self._jenkins_plugin_manager_manager.install(
            config.jenkins.plugin_manager_version
        )

        java_home = self._java_manager.get_home_dir(config.jenkins.java_version)
        jenkins_war = self._jenkins_manager.get_war_file(config.jenkins.version)
        jenkins_plugin_manager_jar = self._jenkins_plugin_manager_manager.get_jar_file(
            config.jenkins.plugin_manager_version
        )

        plugins = [
            f"{plugin}:{name}" for (plugin, name) in config.jenkins.plugins.items()
        ]

        run(
            [
                join(java_home, "bin", "java"),
                "-jar",
                jenkins_plugin_manager_jar,
                "--war",
                jenkins_war,
                "-d",
                join(self._paths_provider.get_jenkins_home_dir(), "plugins"),
                "--plugins",
                *plugins,
            ]
        )


install_command = InstallCommand(
    paths_provider,
    config_provider,
    java_manager,
    jenkins_manager,
    jenkins_plugin_manager_manager,
)
