#!/bin/bash

# Strict mode
set -euo pipefail
IFS=$'\n\t'

# Global constants
readonly SCRIPT_NAME="ServerManagerBot"
readonly INSTALL_DIR="/opt/erfjab"
readonly BRANCH="master"
readonly USERNAME="erfjab"

readonly SERVICE_FILE="/etc/systemd/system/${SCRIPT_NAME}.service"
readonly SERVICE_NAME="${SCRIPT_NAME}.service"
readonly REPO_URL="https://github.com/${USERNAME}/${SCRIPT_NAME}.git"
readonly SCRIPT_URL="https://raw.githubusercontent.com/${USERNAME}/${SCRIPT_NAME}/${BRANCH}/install.sh"
readonly LOG_FILE_ADDRESS="${INSTALL_DIR}/${SCRIPT_NAME}/${SCRIPT_NAME}.log"
readonly ENV_FILE="$INSTALL_DIR/$SCRIPT_NAME/.env"

# ANSI color codes
declare -r -A COLORS=(
    [RED]='\033[0;31m'
    [GREEN]='\033[0;32m'
    [YELLOW]='\033[0;33m'
    [BLUE]='\033[0;34m'
    [RESET]='\033[0m'
)


# Logging functions
log() { printf "${COLORS[BLUE]}[INFO]${COLORS[RESET]} %s\n" "$*"; }
warn() { printf "${COLORS[YELLOW]}[WARN]${COLORS[RESET]} %s\n" "$*" >&2; }
error() { printf "${COLORS[RED]}[ERROR]${COLORS[RESET]} %s\n" "$*" >&2; exit 1; }
success() { printf "${COLORS[GREEN]}[SUCCESS]${COLORS[RESET]} %s\n" "$*"; }

# Error handling
trap 'error "An error occurred. Exiting..."' ERR

# Utility functions
check_root() {
    [[ $EUID -eq 0 ]] || error "This script must be run as root"
}

# Dependency check
declare -a DEPENDENCIES=(
    "git"
    "python3"
    "python3-pip"
    "python3-venv"
    "systemctl"
)

declare -a PIP_DEPENDENCIES=(
    "uv"
)

# Check for missing dependencies and install them
check_system_dependencies() {
    local missing_deps=()
    for dep in "${DEPENDENCIES[@]}"; do
        if ! command -v "$dep" &>/dev/null; then
            missing_deps+=("$dep")
        fi
    done

    # Update package lists and install missing dependencies
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log "Installing missing dependencies: ${missing_deps[*]}"
        apt update && apt install -y "${missing_deps[@]}" || error "Failed to install dependencies."
    else
        success "All dependencies are installed."
    fi
}

# Check for missing pip dependencies and install them
check_pip_dependencies() {
    for package in "${PIP_DEPENDENCIES[@]}"; do
        if ! python3 -c "import $package" &>/dev/null; then
            log "Installing missing pip dependency: $package"
            pip3 install "$package" || error "Failed to install pip dependency: $package"
        else
            success "Pip dependency $package is already installed."
        fi
    done
}

# Run checks
check_dependencies() {
    check_system_dependencies
    check_pip_dependencies
}

check_and_setup_env() {
    if [[ ! -f "$ENV_FILE" ]]; then
        cp $INSTALL_DIR/$SCRIPT_NAME/.env.example $ENV_FILE
        nano $ENV_FILE
    else
        log ".env file already exists."
    fi
}

is_installed() {
    [[ -d "$INSTALL_DIR/$SCRIPT_NAME" && -f "$SERVICE_FILE" ]]
}

is_running() {
    systemctl is-active --quiet "$SERVICE_NAME" || return 1
}


create_directories() {
    local target_dir="$INSTALL_DIR/$SCRIPT_NAME"
    
    if [[ -d "$target_dir" ]]; then
        log "Existing installation directory found at $target_dir"
        log "Removing old installation..."
        rm -rf "$target_dir"
        if [[ $? -ne 0 ]]; then
            error "Failed to remove existing directory. Please check permissions and try again."
        fi
        success "Old installation removed successfully."
    fi

    log "Creating new installation directory..."
    mkdir -p "$target_dir"
    if [[ $? -ne 0 ]]; then
        error "Failed to create directory $target_dir. Please check permissions and try again."
    fi
    
    chmod 750 "$target_dir"
    if [[ $? -ne 0 ]]; then
        error "Failed to set permissions on $target_dir. Please check your user permissions."
    fi
    
    success "Installation directory created successfully at $target_dir"
}

create_service() {
    log "Creating systemd service..."

    if [ -f "$SERVICE_FILE" ]; then
        log "Existing service found. Removing it..."
        systemctl stop "$SERVICE_NAME"
        systemctl disable "$SERVICE_NAME"
        rm -f "$SERVICE_FILE"
        log "Old service removed."
    fi

    cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=$SCRIPT_NAME Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR/$SCRIPT_NAME
ExecStartPre=uv sync
ExecStart=uv run main.py
Restart=always
RestartSec=3
StandardOutput=append:$LOG_FILE_ADDRESS
StandardError=append:$LOG_FILE_ADDRESS

[Install]
WantedBy=multi-user.target
EOF
    chmod 644 "$SERVICE_FILE"
    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    success "Systemd service created and enabled"
}


clone_repo() {
    log "Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR/$SCRIPT_NAME" || error "Failed to clone repository"
    success "Repository cloned successfully"
}

update_repo() {
    log "Updating repository..."
    cd "$INSTALL_DIR/$SCRIPT_NAME"
    git fetch origin
    git reset --hard origin/$BRANCH
    success "Repository updated successfully"
}

manage_service() {
    local action=$1
    if ! is_installed; then
        error "$SCRIPT_NAME is not installed. Please install it first."
    fi
    
    case "$action" in
        start)
            if is_running; then
                warn "$SCRIPT_NAME is already running."
            else
                log "Starting $SCRIPT_NAME service..."
                systemctl start "$SERVICE_NAME" || error "Failed to start $SCRIPT_NAME service"
                success "$SCRIPT_NAME service started"
            fi
            ;;
        stop)
            if is_running; then
                log "Stopping $SCRIPT_NAME service..."
                systemctl stop "$SERVICE_NAME" || error "Failed to stop $SCRIPT_NAME service"
                success "$SCRIPT_NAME service stopped"
            else
                warn "$SCRIPT_NAME is not running."
            fi
            ;;
        restart)
            log "Restarting $SCRIPT_NAME service..."
            systemctl daemon-reload
            systemctl enable "$SERVICE_NAME"
            systemctl restart "$SERVICE_NAME" || error "Failed to restart $SCRIPT_NAME service"
            success "$SCRIPT_NAME service restarted"
            ;;
        *)
            error "Unknown action: $action"
            ;;
    esac
}

show_status() {
    if ! is_installed; then
        error "$SCRIPT_NAME is not installed."
    fi
    systemctl status "$SERVICE_NAME"
}

show_logs() {
    if ! is_installed; then
        error "$SCRIPT_NAME is not installed."
        return
    fi
    
    if [[ -f "$LOG_FILE_ADDRESS" ]]; then
        tail -f "$LOG_FILE_ADDRESS"
    else
        error "Log file not found: $LOG_FILE_ADDRESS"
    fi
}

uninstall_bot() {
    if ! is_installed; then
        error "$SCRIPT_NAME is not installed."
    fi
    log "Uninstalling $SCRIPT_NAME..."
    manage_service "stop"
    systemctl disable "$SERVICE_NAME"
    rm -f "$SERVICE_FILE"
    rm -rf "$INSTALL_DIR/$SCRIPT_NAME"
    systemctl daemon-reload
    success "$SCRIPT_NAME uninstalled successfully"
}

update_bot() {
    if ! is_installed; then
        error "$SCRIPT_NAME is not installed."
    fi
    log "Updating $SCRIPT_NAME..."
    manage_service "stop"
    update_repo
    check_and_setup_env
    manage_service "start"
    success "$SCRIPT_NAME updated successfully"
}

install_script() {
    local install_dir="/usr/local/bin"
    local script_path="$install_dir/$SCRIPT_NAME"
    
    if [[ -f "$script_path" ]]; then
        warn "$SCRIPT_NAME script is already installed in $install_dir. Updating..."
        sudo rm -rf "$script_path"
    else
        log "Installing $SCRIPT_NAME script in $install_dir..."
    fi
    
    curl -L "$SCRIPT_URL" -o "$script_path" || error "Failed to download the script"
    chmod +x "$script_path" || error "Failed to set execute permissions on the script"
    success "$SCRIPT_NAME script installed/updated successfully in $install_dir."
}

update_script() {
    log "Updating $SCRIPT_NAME script..."
    install_script
    success "$SCRIPT_NAME script updated successfully"
}

uninstall_script() {
    local install_dir="/usr/local/bin"
    local script_path="$install_dir/$SCRIPT_NAME"
    
    if [[ -f "$script_path" ]]; then
        log "Uninstalling $SCRIPT_NAME script from $install_dir..."
        rm -f "$script_path" || error "Failed to remove the script"
        success "$SCRIPT_NAME script uninstalled successfully from $install_dir."
    else
        warn "$SCRIPT_NAME script is not installed in $install_dir."
    fi
}

print_help() {
    cat <<EOF
Usage: $SCRIPT_NAME <command>

Commands:
  install-script   Install/Update the script in /usr/local/bin
  install          Install and set up the handler
  start            Start the handler service
  stop             Stop the handler service
  restart          Restart the handler service
  status           Show the status of the handler service
  logs             Show the handler logs
  update           Update the handler from the repository
  update-script    Update the script itself
  uninstall-script Uninstall the script from /usr/local/bin
  uninstall        Uninstall the handler and remove all files
  help             Show this help message

Examples:
  $SCRIPT_NAME install-script
  $SCRIPT_NAME install
  $SCRIPT_NAME start
  $SCRIPT_NAME update

EOF
}

main() {
    check_root

    if [ $# -eq 0 ]; then
        print_help
        exit 0
    fi

    while [ $# -gt 0 ]; do
        case "$1" in
            install-script)
                check_dependencies
                install_script
                ;;
            uninstall-script)
                uninstall_script
                ;;
            install)
                if is_installed; then
                    error "$SCRIPT_NAME is installed. Please uninstall it first."
                fi
                check_dependencies
                create_directories
                clone_repo
                check_and_setup_env
                ;;
            install-service)
                if is_installed; then
                    error "$SCRIPT_NAME is installed. Please uninstall it first."
                fi
                create_service
                ;;
            start)
                manage_service "start"
                show_logs
                ;;
            stop)
                manage_service "stop"
                ;;
            restart)
                manage_service "restart"
                show_logs
                ;;
            status)
                show_status
                ;;
            logs)
                show_logs
                ;;
            env)
                nano $ENV_FILE
                ;;
            update)
                update_bot
                show_logs
                ;;
            update-script)
                update_script
                ;;
            uninstall)
                uninstall_bot
                ;;
            help)
                print_help
                ;;
            *)
                error "Unknown command: $1"
                ;;
        esac
        shift
    done
}

# Execute main function
main "$@"