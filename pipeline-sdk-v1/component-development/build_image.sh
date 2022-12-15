#!/bin/bash -e
container_registry=jackma00
image_name=component-development-test
image_tag=latest
full_image_name=${container_registry}/${image_name}:${image_tag}

cd "$(dirname "$0")" 
docker build --tag "${full_image_name}" .
docker push "${full_image_name}"

# Output the strict image name, which contains the sha256 image digest
docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name}"