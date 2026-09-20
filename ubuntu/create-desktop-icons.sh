#!/bin/sh

# ============================================================
# Ubuntu Desktop Icon Creator
#
# Can be executed from anywhere.
# Desktop icons are ALWAYS created on the current user's Desktop.
# ============================================================

# Make this script executable using below command
# chmod +x create-desktop-icons.sh

set -u

# ------------------------------------------------------------
# Find the user's Desktop directory
# ------------------------------------------------------------

DESKTOP_DIR="$HOME/Desktop"

# Some Ubuntu installations/locales use XDG desktop directory.
if command -v xdg-user-dir >/dev/null 2>&1; then
    XDG_DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null)"

    if [ -n "$XDG_DESKTOP" ] && [ "$XDG_DESKTOP" != "Desktop" ]; then
        DESKTOP_DIR="$XDG_DESKTOP"
    fi
fi

# Create Desktop directory if it does not exist.
mkdir -p "$DESKTOP_DIR"

# ------------------------------------------------------------
# Function: make_launcher
# ------------------------------------------------------------

make_launcher() {
    FILE="$1"
    CONTENT="$2"

    echo "$CONTENT" > "$DESKTOP_DIR/$FILE"

    # Make executable.
    chmod 755 "$DESKTOP_DIR/$FILE"

    # Mark as trusted/allowed to launch in GNOME/Nautilus.
    if command -v gio >/dev/null 2>&1; then
        gio set "$DESKTOP_DIR/$FILE" metadata::trusted true 2>/dev/null || true
    fi

    echo "Created: $DESKTOP_DIR/$FILE"
}

# ------------------------------------------------------------
# Launcher definitions
# ------------------------------------------------------------

RESTART_WITHOUT_CONFIRMATION='[Desktop Entry]
Type=Application
Name=Restart
Exec=systemctl reboot
Icon=system-reboot
Terminal=false'

RESTART_WITH_CONFIRMATION='[Desktop Entry]
Type=Application
Name=Restart
Exec=gnome-session-quit --reboot
Icon=system-reboot
Terminal=false'

POWER_OFF='[Desktop Entry]
Type=Application
Name=Power Options
Exec=gnome-session-quit --power-off
Icon=system-shutdown
Terminal=false'

# ------------------------------------------------------------
# Menu
# ------------------------------------------------------------

show_menu() {
    echo
    echo "=========================================="
    echo "       Ubuntu Desktop Icon Creator"
    echo "=========================================="
    echo
    echo "Desktop directory:"
    echo "  $DESKTOP_DIR"
    echo
    echo "Select an option:"
    echo
    echo "  1) Create Restart icon (with confirmation)"
    echo "  2) Create Restart icon (without confirmation)"
    echo "  3) Create Power Off icon"
    echo "  4) Create ALL icons"
    echo "  5) Exit"
    echo
    printf "Enter your choice [1-5]: "
}

while true
do
    show_menu
    read CHOICE

    case "$CHOICE" in

        1)
            make_launcher \
                "Restart-with-confirmation.desktop" \
                "$RESTART_WITH_CONFIRMATION"

            echo
            echo "Restart icon with confirmation created."
            echo
            ;;

        2)
            make_launcher \
                "Restart-without-confirmation.desktop" \
                "$RESTART_WITHOUT_CONFIRMATION"

            echo
            echo "Restart icon without confirmation created."
            echo
            ;;

        3)
            make_launcher \
                "Power-Off.desktop" \
                "$POWER_OFF"

            echo
            echo "Power Off icon created."
            echo
            ;;

        4)
            make_launcher \
                "Restart-with-confirmation.desktop" \
                "$RESTART_WITH_CONFIRMATION"

            make_launcher \
                "Restart-without-confirmation.desktop" \
                "$RESTART_WITHOUT_CONFIRMATION"

            make_launcher \
                "Power-Off.desktop" \
                "$POWER_OFF"

            echo
            echo "All three icons have been created."
            echo
            ;;

        5)
            echo
            echo "Exiting."
            exit 0
            ;;

        *)
            echo
            echo "Invalid choice. Please enter 1, 2, 3, 4, or 5."
            echo
            ;;

    esac
done
