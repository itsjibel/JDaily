#!/bin/bash

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

# Function to install Python on different distributions
install_python() {
    case "$DISTRO" in
        "ubuntu" | "debian")
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip
            ;;

        "centos" | "rhel" | "fedora")
            sudo yum -y update
            sudo yum install -y python3 python3-pip
            ;;

        "arch")
            sudo pacman -Syu --noconfirm
            sudo pacman -S --noconfirm python python-pip
            ;;

        *)
            echo "Unsupported distribution: $DISTRO"
            exit 1
            ;;
    esac
}

# Function to install PyQt5
install_pyqt5() {
    case "$DISTRO" in
        "ubuntu" | "debian")
            sudo apt-get install -y python3-pyqt5
            ;;

        "centos" | "rhel" | "fedora")
            sudo yum install -y python3-qt5
            ;;

        "arch")
            sudo pacman -S --noconfirm python-pyqt5
            ;;

        *)
            echo "Unsupported distribution: $DISTRO"
            exit 1
            ;;
    esac
}

# Function to compile and create the executable
compile_and_create_executable() {
    chmod +x ../../src/main.py
    echo '#!/bin/bash' > jdaily
    echo 'python3 ../../src/main.py "$@"' >> jdaily
    sudo mv jdaily /usr/bin/
    cd ..
    chmod +x /usr/bin/jdaily
}

# Main execution
detect_distribution
echo "Detected distribution: $DISTRO"
install_python
echo "Python installed successfully!"
install_pyqt5
echo "PyQt5 library installed successfully!"
compile_and_create_executable
echo "Executable 'jdaily' created in /usr/bin/ for running 'main.py'!"