#!/bin/bash

# Function to set environment variables
set_environment() {
    echo "Setting environment variables..."
    #. .venv/bin/activate
    export FLASK_APP=main
    export FLASK_ENV=webapp
}

# Function to run the Flask server
run_server() {
    echo "Running Flask server..."
    flask run
}

# Function to run Flask in debug mode
debug_server() {
    echo "Running Flask in debug mode..."
    flask --app main.py --debug run
}

# Main logic to process arguments
case "$1" in
    export)
        set_environment
        ;;
    run)
        set_environment
        run_server
        ;;
    debug)
        set_environment
        debug_server
        ;;
    *)
        echo "Usage: $0 {export|run|debug}"
        exit 1
esac