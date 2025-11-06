
"""PyInstaller build script for MC Clicker."""

import os
import platform
import shutil
import subprocess
import sys


def build_executable() -> None:
    """
    Build the MC Clicker executable using PyInstaller.

    Reason:
        PyInstaller packages Python apps into standalone executables. We use
        specific flags to minimize size and create a single file.
    """
    # Check if PyInstaller is installed
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            check=True,
        )

    # Clean up previous builds
    for folder in ["MCClicker", "dist", "__pycache__"]:
        folder_path = os.path.join(os.path.dirname(__file__), folder)
        if os.path.exists(folder_path):
            print(f"Removing {folder}...")
            shutil.rmtree(folder_path)

    # Determine separator for --add-data (Windows uses ;, Unix uses :)
    sep = ";" if platform.system() == "Windows" else ":"

    # PyInstaller command
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name=MCClicker",  # Executable name
        "--clean",  # Clean temp files
        "-y",  # Overwrite output
        f"--add-data=src{sep}src",  # Include src package
        "src/main.py",  # Entry point
    ]

    # Add icon if it exists
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    if os.path.exists(icon_path):
        pyinstaller_cmd.insert(3, f"--icon={icon_path}")

    print("Building executable...")
    print(" ".join(pyinstaller_cmd))
    result = subprocess.run(pyinstaller_cmd, check=False)

    if result.returncode != 0:
        print("Build failed!")
        sys.exit(1)

    # Check output size
    exe_path = "dist/MCClicker.exe"
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print("\n[SUCCESS] Build successful!")
        print(f"[OUTPUT] {exe_path}")
        print(f"[SIZE] {size_mb:.2f} MB")

        if size_mb > 20:
            print(
                "\n[WARNING] Executable is larger than 20MB. "
                "Consider using UPX for compression."
            )
    else:
        print("Build completed but executable not found!")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()

