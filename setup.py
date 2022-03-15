from typing import Iterator
from setuptools import setup, find_namespace_packages  # type: ignore


# TODO: should probably migrate to src/promnesia_sean to fix this issue?
def subpackages() -> Iterator[str]:
    for p in find_namespace_packages("."):
        if p.startswith("promnesia_sean"):
            yield p


def main() -> None:
    pkg = "promnesia_sean"
    pkgs = list(subpackages())
    setup(
        name=pkg,
        zip_safe=False,
        packages=pkgs,
        package_data={pkg: ["py.typed"]},
        url="https://github.com/seanbreckenridge/promnesia",
        author="Sean Breckenridge",
        author_email="seanbrecke@gmail.com",
    )


if __name__ == "__main__":
    main()
