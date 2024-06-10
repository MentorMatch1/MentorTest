#!/bin/bash

echo "Starting Ollama"
# Start the ollama service
ollama start &

# Wait for ollama to be ready
echo "ollama is up - fetching model"
sleep 5
# Fetch the model
ollama pull mxbai-embed-large

if ollama pull mxbai-embed-large; then
  echo "Model mxbai-embed-large fetched successfully"
else
  echo "Failed to fetch model mxbai-embed-large" && exit 1
fi

# Run the main application
exec "$@"