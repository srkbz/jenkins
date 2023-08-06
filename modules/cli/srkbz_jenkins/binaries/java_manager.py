import platform
from os import makedirs, symlink, remove
from os.path import join, isfile, isdir, exists
from pathlib import Path
from dataclasses import dataclass, asdict
import tarfile
import shutil
import json

import requests

from srkbz_jenkins.paths.paths_provider import PathsProvider, paths_provider
from srkbz_jenkins.utils.download_file import download_file


@dataclass
class _PackageInfo:
    url: str
    home_path: str


_adoptium_platform_mapper = {"Darwin_arm64": ("mac", "aarch64", "Contents/Home")}


class JavaManager:
    def __init__(self, paths_provider: PathsProvider) -> None:
        self._paths_provider = paths_provider

    def install(self, version: str):
        binaries_dir = self._paths_provider.get_binaries_dir()

        version_dir = join(binaries_dir, "java", version)
        package_dir = join(version_dir, "package")
        package_contents_dir = join(package_dir, "contents")
        package_file = join(package_dir, "package.tar.gz")
        package_info_file = join(package_dir, "info.json")
        home_dir = join(version_dir, "home")

        if not exists(package_info_file):
            package_info = self._get_package_info(version)
            with open(package_info_file, "w") as f:
                f.write(json.dumps(asdict(package_info), indent=2))
        else:
            with open(package_info_file, "r") as f:
                package_info = _PackageInfo(**json.loads(f.read()))

        if not exists(package_file):
            makedirs(package_dir, exist_ok=True)
            download_file(
                package_info.url,
                package_file,
                f"Java {version}",
            )
            shutil.rmtree(package_contents_dir, ignore_errors=True)

        if not exists(package_contents_dir):
            makedirs(package_contents_dir, exist_ok=True)
            package = tarfile.open(package_file)
            package.extractall(package_contents_dir)
            shutil.rmtree(home_dir, ignore_errors=True)

        if not exists(home_dir):
            symlink(join(package_contents_dir, package_info.home_path), home_dir)

    def _get_package_info(self, version: str) -> _PackageInfo:
        adoptium_api_url = self._get_adoptium_api_url(version)
        response = requests.get(
            adoptium_api_url,
            headers={
                "User-Agent": "fuck you azure https://stackoverflow.com/a/71292611"
            },
            allow_redirects=True,
        )

        system_os = platform.system()
        system_arch = platform.machine()
        (_, _, home_path) = _adoptium_platform_mapper[f"{system_os}_{system_arch}"]

        for item in response.json():
            if item["binary"]["image_type"] == "jdk":
                return _PackageInfo(
                    url=item["binary"]["package"]["link"],
                    home_path=item["release_name"] + "/" + home_path,
                )

        raise Exception("Could not find a compatible Java package")

    def _get_adoptium_api_url(self, version: str) -> str:
        system_os = platform.system()
        system_arch = platform.machine()
        adoptium_platform = _adoptium_platform_mapper[f"{system_os}_{system_arch}"]

        if adoptium_platform is None:
            raise Exception(f"Unsupported platform: {system_os} {system_arch}")

        (adoptium_os, adoptium_arch, _) = adoptium_platform
        return f"https://api.adoptium.net/v3/assets/latest/{version}/hotspot?os={adoptium_os}&architecture={adoptium_arch}"


java_manager = JavaManager(paths_provider)
