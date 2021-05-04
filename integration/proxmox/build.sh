#!/bin/bash
GIT_SHA=$(git rev-parse HEAD | cut -c 1-8)
IMAGE="jeremykuhnash/integration-machine-listener:$GIT_SHA"
IMAGE_LATEST="jeremykuhnash/integration-machine-listener:latest"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
THIS_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
# echo "This Dir: $THIS_DIR"

docker build -t $IMAGE -t $IMAGE_LATEST -f Dockerfile .

## TODO: Switch logic if "CI=true" is set eg do diff stuff during CI/CD build.
# docker push $IMAGE
# docker push $IMAGE_LATEST