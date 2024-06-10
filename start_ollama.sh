#!/bin/bash

echo "Starting Ollama"
# Start the ollama service
ollama start &
echo "ollama is up"

exec "$@"