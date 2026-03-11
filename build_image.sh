#!/bin/bash

# Default version if not provided
VERSION=${1:-"v1.0.0"}
IMAGE_NAME="flask-notes-app"

echo "Building Docker image: $IMAGE_NAME with version: $VERSION"

# Build the image and tag it
docker build -t "$IMAGE_NAME:$VERSION" -t "$IMAGE_NAME:latest" .

echo "Successfully built $IMAGE_NAME:$VERSION and $IMAGE_NAME:latest"
