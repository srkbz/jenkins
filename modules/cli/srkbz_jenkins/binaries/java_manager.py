import platform
from os import makedirs
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
        binaries_dir = self._paths_provider.get_binaries_dir()
        installation_dir = join(binaries_dir, "java", version, "packages")
        package_info = self._get_package_info(version)
        makedirs(installation_dir, exist_ok=True)

        downloaded = 0
        with open(join(installation_dir, "package.tar.gz"), "wb") as f:
            response = requests.get(package_info.url, allow_redirects=True, stream=True)
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                downloaded += len(data)
                print(downloaded)

    def _get_package_info(self, version: str) -> _PackageInfo:
        adoptium_api_url = self._get_adoptium_api_url(version)
        response = requests.get(
            adoptium_api_url,
            headers={
                "User-Agent": "fuck you azure https://stackoverflow.com/a/71292611"
            },
            allow_redirects=True,
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
