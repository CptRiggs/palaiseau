"""Package paraser"""

import tarfile
import json

from palaiseau.exceptions import InvalidPackageException


class Package:
    """Package handler"""

    def __init__(self, path) -> None:
        self._tar = tarfile.open(path, "r:*") # pylint: disable=R1732
        build_file = self._tar.extractfile("./.build.json")
        if build_file is not None:
            build_json = json.loads(build_file.read().decode("utf-8"))
            self._dict = build_json
        else:
            raise InvalidPackageException

    def get_tar(self) -> tarfile.TarFile:
        """Returns package tar file"""

        return self._tar

    def get_buildfl(self) -> dict:
        """Returns package build.json"""

        return self._dict
