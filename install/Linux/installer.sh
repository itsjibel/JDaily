#!/bin/bash

# Activate your Python environment, if you have one.
# source "/.../venv/bin/activate"

# Check if the script is run with superuser privileges
check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        echo "Error: This script requires superuser privileges. Please run with 'sudo'."
        exit 1
    fi
}

# Function to detect the Linux distribution
detect_distribution() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO="$ID"
    elif [ -f /etc/debian_version ]; then
        DISTRO="debian"
    elif [ -f /etc/redhat-release ]; then
        DISTRO="redhat"
    else
        DISTRO="unknown"
    fi
}

# Function to install required packages
install_packages() {
    case "$DISTRO" in
        "ubuntu" | "debian")
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-pyqt5
            ;;

        "centos" | "rhel" | "fedora")
            sudo yum -y update
            sudo yum install -y python3 python3-pip python3-qt5
            ;;

        "arch")
            sudo pacman -Syu --noconfirm
            sudo pacman -S --noconfirm python python-pip python-pyqt5
            ;;

        *)
            echo "Unsupported distribution: $DISTRO"
            exit 1
            ;;
    esac
}

# Function to install PyInstaller
install_pyinstaller() {
    echo "Installing PyInstaller..."
    sudo pip3 install pyinstaller
}

# Function to compile using PyInstaller
compile_using_pyinstaller() {
    cd ../../src
    pyinstaller --onefile main.py
    sudo mv dist/main /usr/bin/jdaily
    echo "Executable 'jdaily' created in /usr/bin/ for running 'main.py'!"
}

# Main execution
check_sudo
detect_distribution
echo "Detected distribution: $DISTRO"
install_packages

# Check if PyInstaller is installed, install if not
if ! command -v pyinstaller &> /dev/null; then
    install_pyinstaller
fi

compile_using_pyinstaller
