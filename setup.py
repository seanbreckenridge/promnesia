from setuptools import setup, find_namespace_packages  # type: ignore


def main() -> None:
    pkg = "promnesia"
    pkgs = find_namespace_packages(include=[pkg])
    print(pkgs)
    setup(
        name=f"{pkg}-seanbreckenridge",
        zip_safe=False,
        packages=pkgs,
        package_data={pkg: ["py.typed"]},
        url="https://github.com/seanbreckenridge/promnesia",
        author="Sean Breckenridge",
        author_email="seanbrecke@gmail.com",
        python_requires=">=3.6",
        install_requires=[],
    )


if __name__ == "__main__":
    main()
