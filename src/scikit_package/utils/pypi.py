import requests
from packaging.version import parse as parse_version


def get_pypi_version_sha(package_name, count=1):
    """Fetch the latest stable versions of the package and their SHA256."""
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    if response.status_code == 200:
        data = response.json()
        all_versions = [
            v
            for v in data["releases"].keys()
            if not parse_version(v).is_prerelease
        ]
        sorted_versions = sorted(
            all_versions, key=parse_version, reverse=True
        )[:count]
        version_info = {}
        for version in sorted_versions:
            files = data["releases"][version]
            for file in files:
                if file["packagetype"] == "sdist":
                    version_info[version] = file["digests"]["sha256"]
                    break
        return version_info
    else:
        raise ValueError(
            f"No matching package found for {package_name} on PyPI. "
            "Please check the name at https://pypi.org/project/"
        )
