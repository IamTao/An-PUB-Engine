#!/bin/bash

for i in "$@"
do
case $i in
    -t=*|--tag=*)
    TAG="${i#*=}"
    shift 
    ;;
    --publish*)
    PUBLISH=true
    shift 
    ;;
    *)
    ;;
esac
done

TAG=${TAG:-latest}
PUBLISH=${PUBLISH:-false}

sudo docker build -t daunnc/serf:${TAG} .

if ${PUBLISH}; then
  sudo docker push daunnc/serf:${TAG}
fi
