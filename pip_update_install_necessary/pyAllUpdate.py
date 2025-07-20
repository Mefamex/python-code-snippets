#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pyallupdate
-----------
A handy tool to update all installed pip packages and your selected package lists.
It also exports the list of all packages to a .txt file.

Author      : mefamex   (https://mefamex.com)
Copyright   : MIT
Status      : Prototype
Created     : 2025-07-18
Requires    : Python 3.8+
Version     : 1.0.0 : 2025-07-18 -> Initial version
"""

import os, sys, logging, pkg_resources, subprocess
from pathlib import Path
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


# ----------- Logger Configuration --------------

logger = logging.getLogger("pyallupdate")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


# ----------- pyAllUpdate Class -----------------

class PyAllUpdate:
    """
    Updates pip packages in bulk or from a selected file.
    """

    @staticmethod
    def update_package(package_name: str) -> bool:
        """Updates a single package."""
        try:
            logger.info(f"Updating package: {package_name}")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", package_name],
                capture_output=True, text=True, check=True
            )
            logger.info(f"Package '{package_name}' updated successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error updating '{package_name}': {e.stdout} {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Unknown error updating '{package_name}': {str(e)}")
            return False

    @staticmethod
    def update_packages(packages: List[str], parallelism: int = 5) -> bool:
        """Updates multiple packages using multithreading."""
        if not packages:
            logger.warning("No packages to update.")
            return False
        logger.info(f"Total packages to update: {len(packages)}")
        update_any = False
        with ThreadPoolExecutor(max_workers=parallelism) as executor:
            futures = {executor.submit(PyAllUpdate.update_package, pkg): pkg for pkg in packages}
            for future in as_completed(futures):
                package = futures[future]
                try:
                    result = future.result()
                    update_any = update_any or result
                except Exception as exc:
                    logger.error(f"Exception updating '{package}': {exc}")
        return update_any

    @staticmethod
    def list_installed_packages(write_to: Optional[Path] = None) -> List[str]:
        """Returns all installed packages and optionally writes them to a file."""
        packages = sorted({dist.project_name for dist in pkg_resources.working_set})
        logger.info(f"Installed packages found: {len(packages)}")
        if write_to:
            with open(write_to, 'w', encoding='utf-8') as f:
                for package in packages:
                    f.write(package + '\n')
            logger.info(f"Installed packages list written to '{write_to}'")
        return packages

    @staticmethod
    def update_all_installed() -> bool:
        """Updates all packages installed in the system."""
        packages = PyAllUpdate.list_installed_packages(write_to=Path("installed_packages.txt"))
        if not packages:
            logger.warning("No installed packages found!")
            return False
        return PyAllUpdate.update_packages(packages)


def choose_text_file(files: List[Path]) -> Optional[Path]:
    """Lists available .txt files and lets the user select one."""
    print(f"\nListed .txt files ({len(files)} found):")
    for idx, file in enumerate(files):
        print(f"{idx}: {file}")
    while True:
        try:
            choice = input("Which file should be used to update packages? [number]: ").strip()
            if choice.isdigit() and 0 <= int(choice) < len(files):
                return files[int(choice)]
            print("Invalid selection, please try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)


def main():
    os.chdir(Path(__file__).parent.resolve())

    # 1. First, update all installed packages
    print("Updating all installed packages...")
    if not PyAllUpdate.update_all_installed():
        logger.warning("Some packages could not be updated or none were updated.")
    else:
        print("All installed packages have been updated.")

    # 2. Find .txt files, let the user select one, and update packages from the list
    txt_files = [p.resolve() for p in Path('.').glob("*.txt")]
    if not txt_files:
        print("\nNo .txt files found.")
        sys.exit(1)
    selected_file = choose_text_file(txt_files)
    if not selected_file:
        print("No file selected. Exiting.")
        sys.exit(1)
    with open(selected_file, 'r', encoding='utf-8') as f:
        packages = [line.strip() for line in f if line.strip()]
    if not packages:
        print("No packages found in the selected file.")
        sys.exit(1)
    print(f"\nNumber of packages to update from the selected file: {len(packages)}\n")
    if PyAllUpdate.update_packages(packages):
        print("The specified packages have been updated successfully.")
    else:
        print("Some packages could not be updated.")

    print("Program is terminating.")


if __name__ == "__main__":
    main()
