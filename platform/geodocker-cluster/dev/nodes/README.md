# Nodes.

Provides accumulo configuration files to maintain Accumulo with one ZooKeeper node.

## Build Serf

You can build and publish single-node images (master and slave) using `build.sh` script:

```bash
  Options:
    -a=<1.6.x | 1.7.x> | --accumulo=<1.6.x | 1.7.x>  Accumulo version [default: 1.7.0]
    -t=<tag> | --tag=<tag>                           Image tag [default: latest].
    -bt=<tag> | --base-tag=<tag>                     Base image tag [default: latest].
    --build-base                                     Build base image if it is not build.
    --publish                                        Push container to dockerhub.
```

## Start cluster

You can start cluster using `./start-cluster.sh` script:

```bash
  Options:
    -n=<n> | --nodes=<n>             Nodes amount [n >= 1].
    -t=<tag> | --tag=<tag>           Image tag to start [default: latest].    
    -v=<volume> | --volume=<volume>  Mounts absolute `volume path` to a `/data` container folder.
```

## Add slave

You can add slave node to already launched master:

```bash
  Options:
    -t=<tag> | --tag=<tag>             Image tag to start [default: latest].    
    -n=<name> | --name=<n>             Slave image name.
    -h=<hostname> | --host=<hostname>  Slave hostname, should end with `.gt` (*slave50.gt*).  
    -v=<volume> | --volume=<volume>    Mounts absolute `volume path` to a `/data` container folder.  
```
