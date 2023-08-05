import platform
from os.path import join
from dataclasses import dataclass

import requests

from srkbz_jenkins.paths.paths_provider import PathsProvider, paths_provider


@dataclass
class _PackageInfo:
    url: str


_adoptium_platform_mapper = {"Darwin_arm64": ("mac", "aarch64")}


class JavaManager:
    def __init__(self, paths_provider: PathsProvider) -> None:
        self._paths_provider = paths_provider

    def install(self, version: str):
        print(join(self._paths_provider.get_binaries_dir(), "java", version))
        print(self._get_package_info(version))

    def _get_package_info(self, version: str) -> _PackageInfo:
        adoptium_api_url = self._get_adoptium_api_url(version)
        response = requests.get(
            adoptium_api_url,
            headers={
                "User-Agent": "fuck you azure https://stackoverflow.com/a/71292611"
            },
        )

        for item in response.json():
            if item["binary"]["image_type"] == "jdk":
                return _PackageInfo(url=item["binary"]["package"]["link"])

        raise Exception("Could not find a compatible Java package")

    def _get_adoptium_api_url(self, version: str) -> str:
        system_os = platform.system()
        system_arch = platform.machine()
        adoptium_platform = _adoptium_platform_mapper[f"{system_os}_{system_arch}"]

        if adoptium_platform is None:
            raise Exception(f"Unsupported platform: {system_os} {system_arch}")

        (adoptium_os, adoptium_arch) = adoptium_platform
        return f"https://api.adoptium.net/v3/assets/latest/{version}/hotspot?os={adoptium_os}&architecture={adoptium_arch}"


java_manager = JavaManager(paths_provider)
