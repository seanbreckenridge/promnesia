from setuptools import setup, find_namespace_packages  # type: ignore


def main() -> None:
    pkg = "promnesia"
    pkgs = find_namespace_packages(include=[pkg])
    setup(
        name=f"{pkg}-seanbreckenridge",
        zip_safe=False,
        packages=pkgs,
        url="https://github.com/seanbreckenridge/promnesia",
        author="Sean Breckenridge",
        author_email="seanbrecke@gmail.com",
    )


if __name__ == "__main__":
    main()
