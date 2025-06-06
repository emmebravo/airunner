#!/bin/bash
set -e
set -x

# Try to find Python 3.13.3 - check various possible locations
PYTHON_CMD=""

# Check common locations for Python 3.13.3
if [ -x "/usr/local/bin/python3.13" ]; then
    PYTHON_CMD="/usr/local/bin/python3.13"
    echo "Found Python at /usr/local/bin/python3.13"
elif [ -x "/usr/local/bin/python" ]; then
    PYTHON_CMD="/usr/local/bin/python"
    echo "Found Python at /usr/local/bin/python"
elif [ -x "/usr/bin/python3.13" ]; then
    PYTHON_CMD="/usr/bin/python3.13"
    echo "Found Python at /usr/bin/python3.13"
elif command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
    echo "Using python3 from PATH"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
    echo "Using python from PATH"
else
    echo "WARNING: Could not find Python 3.13.3. Will attempt to continue anyway."
    PYTHON_CMD="python3"  # Default to python3 and hope for the best
fi

# Check Python version
echo "===== Python Version Check ====="
if [ -n "$PYTHON_CMD" ]; then
    $PYTHON_CMD --version || echo "Failed to get Python version"
    
    # Find pip corresponding to Python
    if [ -x "/usr/local/bin/pip3.13" ]; then
        PIP_CMD="/usr/local/bin/pip3.13"
    elif [ -x "/usr/local/bin/pip" ]; then
        PIP_CMD="/usr/local/bin/pip"
    elif command -v pip3 &>/dev/null; then
        PIP_CMD="pip3"
    else
        PIP_CMD="pip"
    fi
    
    $PIP_CMD --version || echo "Failed to get pip version"
else
    echo "No Python executable found to check version."
fi

# Set PYTHONUSERBASE to ensure pip installs packages into the correct directory
export PATH=/usr/local/bin:/home/appuser/.local/share/airunner/python/bin:/home/appuser/.local/bin:$PATH
export PATH=$PYTHONUSERBASE/bin:$PATH

# Remove PIP_USER to avoid conflicts with --prefix
unset PIP_USER

# Ensure pip uses the correct cache directory
export PIP_CACHE_DIR=$AIRUNNER_HOME_DIR/.cache/pip

echo "PATH set to $PATH"
echo "PIP_CACHE_DIR set to $PIP_CACHE_DIR"

# Check if the directory structure exists, but don't try to create it
# if we don't have permission (the host should create these directories)
if [ ! -d "$PYTHONUSERBASE" ]; then
    echo "Warning: PYTHONUSERBASE directory ($PYTHONUSERBASE) does not exist"
    echo "The host should create this directory before running the container"
else
    # Check if subdirectories exist and try to create them only if we have permission
    for dir in bin lib share; do
        if [ ! -d "$PYTHONUSERBASE/$dir" ]; then
            echo "Directory $PYTHONUSERBASE/$dir doesn't exist, attempting to create..."
            mkdir -p "$PYTHONUSERBASE/$dir" 2>/dev/null || echo "Warning: Cannot create $PYTHONUSERBASE/$dir (permission denied, continuing anyway)"
        fi
    done
fi

echo "===== Wayland Setup Information ====="
echo "User: $(whoami)"
echo "XDG_SESSION_TYPE: $XDG_SESSION_TYPE"
echo "QT_QPA_PLATFORM: $QT_QPA_PLATFORM"
echo "GDK_BACKEND: $GDK_BACKEND"

# Package installations have been moved to Dockerfile
# Any runtime-specific setup should go here

# Handle interactive sessions
if [ "$#" -eq 0 ]; then
  echo "No command provided. Starting an interactive shell..."
  exec bash
elif [ "$1" == "airunner" ]; then
  echo "Running airunner in development mode..."
  shift # Remove 'airunner' from the arguments
  cd /app && exec $PYTHON_CMD src/airunner/main.py "$@"
else
  echo "Executing command: $@"
  exec "$@"
fi