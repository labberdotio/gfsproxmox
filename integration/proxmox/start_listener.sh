#!/bin/bash
#
# This is safe to use because ISC DHCPd will not respond to DHCP requests on a non-configured subnet.
# Docker doesn't support specifying --net=host + --ip=IP_ADDR (probably because Docker sucks - there's no good reason that it shouldn't work).
# An option would be to firewall off Client Broadcast UDP packets on the interface - https://support.microsoft.com/en-us/help/169289/dhcp-dynamic-host-configuration-protocol-basics
# In other words, this can run this on the 'dev' systems that have an interface on usual home network (192.168.0.x)
# as well as serve up IP addresses on the cluster network (10.88.88.x)
set -e

CONTAINER_NAME="dhcp"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
THIS_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
echo "This Dir: $THIS_DIR"
source $THIS_DIR/common.sh

docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true
docker pull $DOCKER_IMAGE_DHCP || true
docker run \
  --restart unless-stopped \
  -d \
  --net=host \
  -v /gfs/devBotcanicsDHCP.ISCDHCPService:/etc/dhcp/dhcpd.conf \
  --name $CONTAINER_NAME $DOCKER_IMAGE_DHCP
docker logs $CONTAINER_NAME -f &
#  -v /gfs/devBotcanicsDHCP.ISCDHCPService:/etc/dhcp/dhcpd.conf \
#   -v $THIS_DIR/etc/dhcp:/etc/dhcp \

# Note: So why not just run this manually without daemonizing?
# This way, you can use the script, break out of the log view and its still running.
# The daemon takes 10 seconds to stop either way, still have it running during your shell reboot etc
# just seems more logical for stuff.
echo "To start log viewing again punch in: docker logs $CONTAINER_NAME -f"
