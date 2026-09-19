#!/usr/bin/env bash

set -e

# ============================================================
# Python Environment Manager for Ubuntu
#
# Usage:
#   ./python-env.sh
#   ./python-env.sh --install 3.12
#   ./python-env.sh --venv
#   ./python-env.sh --requirements
#   ./python-env.sh --activate
#   ./python-env.sh --all
#   ./python-env.sh --help
#
# The virtual environment is created in the directory where
# this script is located.
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

header() {
    echo
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}============================================================${NC}"
    echo
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# ------------------------------------------------------------
# Show installed Python versions
# ------------------------------------------------------------

show_python_versions() {
    header "Installed Python Versions"

    local found=0

    for version in 3.8 3.9 3.10 3.11 3.12 3.13 3.14; do
        if command_exists "python$version"; then
            echo -e "${GREEN}Python $version${NC}: $(python$version --version 2>&1)"
            found=1
        fi
    done

    if command_exists python3; then
        echo
        echo "Default python3:"
        python3 --version
        echo "Location: $(command -v python3)"
    fi

    if command_exists python; then
        echo
        echo "Default python:"
        python --version 2>&1
        echo "Location: $(command -v python)"
    fi

    if [ "$found" -eq 0 ]; then
        warning "No supported Python versions were detected."
    fi
}

# ------------------------------------------------------------
# Check Python 3.12
# ------------------------------------------------------------

check_python_312() {
    if command_exists python3.12; then
        success "Python 3.12 is already installed."
        python3.12 --version
        return 0
    fi

    warning "Python 3.12 is not installed."
    return 1
}

# ------------------------------------------------------------
# Install Python version
# ------------------------------------------------------------

install_python() {
    local version="$1"

    if ! [[ "$version" =~ ^3\.[0-9]+$ ]]; then
        error "Invalid Python version: $version"
        return 1
    fi

    if command_exists "python$version"; then
        success "Python $version is already installed."
        "python$version" --version
        return 0
    fi

    header "Installing Python $version"

    info "Updating package information..."

    sudo apt update

    info "Installing Python $version..."

    if sudo apt install -y "python$version" "python$version-venv" "python$version-dev"; then
        success "Python $version installed successfully."
        "python$version" --version
    else
        error "Could not install Python $version from the configured Ubuntu repositories."
        echo
        echo "Your Ubuntu release may not provide this version directly."
        echo "You may need an additional Python repository or another installation method."
        return 1
    fi
}

# ------------------------------------------------------------
# Select Python version interactively
# ------------------------------------------------------------

select_python_version() {
    header "Select Python Version"

    echo "Available choices:"
    echo
    echo "  1) Python 3.12"
    echo "  2) Python 3.13"
    echo "  3) Python 3.14"
    echo "  4) Cancel"
    echo

    read -rp "Select [1-4]: " choice

    case "$choice" in
        1)
            SELECTED_PYTHON="3.12"
            ;;
        2)
            SELECTED_PYTHON="3.13"
            ;;
        3)
            SELECTED_PYTHON="3.14"
            ;;
        4)
            info "Cancelled."
            return 1
            ;;
        *)
            error "Invalid selection."
            return 1
            ;;
    esac

    echo
    info "Selected Python $SELECTED_PYTHON"
}

# ------------------------------------------------------------
# Create virtual environment
# ------------------------------------------------------------

create_virtualenv() {
    local version="$1"

    header "Create Virtual Environment"

    if ! command_exists "python$version"; then
        error "Python $version is not installed."
        echo
        echo "Install it first with:"
        echo "  $0 --install $version"
        return 1
    fi

    if [ -d "$VENV_DIR" ]; then
        warning "Virtual environment already exists:"
        echo "  $VENV_DIR"
        echo

        read -rp "Recreate it? [y/N]: " answer

        if [[ "$answer" =~ ^[Yy]$ ]]; then
            info "Removing existing virtual environment..."
            rm -rf "$VENV_DIR"
        else
            info "Keeping existing virtual environment."
            return 0
        fi
    fi

    info "Creating virtual environment using Python $version..."

    "python$version" -m venv "$VENV_DIR"

    success "Virtual environment created:"
    echo "  $VENV_DIR"
}

# ------------------------------------------------------------
# Install requirements
# ------------------------------------------------------------

install_requirements() {
    header "Install Requirements"

    if [ ! -d "$VENV_DIR" ]; then
        error "Virtual environment does not exist."
        echo
        echo "Create it first with:"
        echo "  $0 --venv"
        return 1
    fi

    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        warning "requirements.txt was not found."
        echo
        echo "Expected:"
        echo "  $REQUIREMENTS_FILE"
        return 0
    fi

    info "Activating virtual environment..."

    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"

    info "Upgrading pip..."

    python -m pip install --upgrade pip

    info "Installing dependencies from requirements.txt..."

    python -m pip install -r "$REQUIREMENTS_FILE"

    success "Requirements installed successfully."
}

# ------------------------------------------------------------
# Activate virtual environment
# ------------------------------------------------------------

activate_virtualenv() {
    header "Activate Virtual Environment"

    if [ ! -d "$VENV_DIR" ]; then
        error "Virtual environment does not exist."
        echo
        echo "Create it first with:"
        echo "  $0 --venv"
        return 1
    fi

    echo
    info "Activating:"
    echo "  $VENV_DIR"
    echo

    # IMPORTANT:
    # This only affects the current shell when the script is
    # sourced rather than executed.
    #
    # If executed as:
    #   ./python-env.sh --activate
    #
    # the parent shell cannot be modified.
    #
    # Therefore we provide the activation command instead.

    echo -e "${GREEN}Run this command in your shell:${NC}"
    echo
    echo "  source \"$VENV_DIR/bin/activate\""
    echo

    echo "Or:"
    echo
    echo "  . \"$VENV_DIR/bin/activate\""
    echo
}

# ------------------------------------------------------------
# Show help
# ------------------------------------------------------------

show_help() {
    cat <<EOF

Python Environment Manager
==========================

Usage:

  $0
      Interactive menu.

  $0 --status
      Show installed Python versions.

  $0 --install VERSION
      Install a Python version.

      Example:
        $0 --install 3.12

  $0 --venv
      Create .venv in the directory where this script exists.

  $0 --venv VERSION
      Create .venv using a specific Python version.

      Example:
        $0 --venv 3.12

  $0 --requirements
      Install dependencies from requirements.txt
      into the local .venv.

  $0 --activate
      Show the command needed to activate .venv.

  $0 --all VERSION
      Install Python, create .venv and install requirements.

      Example:
        $0 --all 3.12

  $0 --help
      Show this help.

Directory:

  Script directory:
    $SCRIPT_DIR

  Virtual environment:
    $VENV_DIR

  Requirements:
    $REQUIREMENTS_FILE

Examples:

  ./python-env.sh

  ./python-env.sh --status

  ./python-env.sh --install 3.12

  ./python-env.sh --venv 3.12

  ./python-env.sh --requirements

  ./python-env.sh --activate

  ./python-env.sh --all 3.12

EOF
}

# ------------------------------------------------------------
# Interactive menu
# ------------------------------------------------------------

interactive_menu() {
    header "Python Environment Manager"

    echo "Script location:"
    echo "  $SCRIPT_DIR"
    echo

    show_python_versions

    echo
    header "Options"

    echo "  1) Check Python 3.12"
    echo "  2) Install Python version"
    echo "  3) Create virtual environment"
    echo "  4) Install requirements.txt"
    echo "  5) Show activation command"
    echo "  6) Do everything"
    echo "  7) Exit"
    echo

    read -rp "Select [1-7]: " choice

    case "$choice" in

        1)
            check_python_312 || true
            ;;

        2)
            select_python_version || return
            install_python "$SELECTED_PYTHON"
            ;;

        3)
            select_python_version || return

            if ! command_exists "python$SELECTED_PYTHON"; then
                warning "Python $SELECTED_PYTHON is not installed."
                read -rp "Install it now? [Y/n]: " answer

                if [[ ! "$answer" =~ ^[Nn]$ ]]; then
                    install_python "$SELECTED_PYTHON"
                else
                    return
                fi
            fi

            create_virtualenv "$SELECTED_PYTHON"
            ;;

        4)
            install_requirements
            ;;

        5)
            activate_virtualenv
            ;;

        6)
            select_python_version || return

            if ! command_exists "python$SELECTED_PYTHON"; then
                warning "Python $SELECTED_PYTHON is not installed."
                install_python "$SELECTED_PYTHON"
            fi

            create_virtualenv "$SELECTED_PYTHON"

            if [ -f "$REQUIREMENTS_FILE" ]; then
                install_requirements
            else
                warning "requirements.txt not found. Skipping dependency installation."
            fi

            activate_virtualenv
            ;;

        7)
            echo "Bye!"
            exit 0
            ;;

        *)
            error "Invalid selection."
            ;;
    esac
}

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

case "${1:-}" in

    "")
        interactive_menu
        ;;

    --status|-s)
        show_python_versions
        ;;

    --install|-i)
        if [ -z "${2:-}" ]; then
            error "Please specify a Python version."
            echo
            echo "Example:"
            echo "  $0 --install 3.12"
            exit 1
        fi

        install_python "$2"
        ;;

    --venv|-v)
        VERSION="${2:-3.12}"

        if ! command_exists "python$VERSION"; then
            warning "Python $VERSION is not installed."
            install_python "$VERSION"
        fi

        create_virtualenv "$VERSION"
        ;;

    --requirements|-r)
        install_requirements
        ;;

    --activate|-a)
        activate_virtualenv
        ;;

    --all)
        VERSION="${2:-3.12}"

        if ! command_exists "python$VERSION"; then
            install_python "$VERSION"
        fi

        create_virtualenv "$VERSION"

        if [ -f "$REQUIREMENTS_FILE" ]; then
            install_requirements
        else
            warning "requirements.txt not found."
        fi

        activate_virtualenv
        ;;

    --help|-h)
        show_help
        ;;

    *)
        error "Unknown option: $1"
        echo
        show_help
        exit 1
        ;;

esac
