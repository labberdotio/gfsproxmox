# ENV Vars which are set by the start script, generally this mimics cloud native 
#   as ENV vars are passed into container orchestrators as settings too or in vault etc.  

export TEST_TEMPLATE_TYPE=""
export TEST_INSTANCE_TYPE=""

export PROXMOX_API_HOST='192.168.56.180'
export PROXMOX_API_PORT='8006'
export PROXMOX_API = "https://" + PROXMOX_API_HOST + ":" PROXMOX_API_PORT
export PROXMOX_POOL = "botcanics"
export PROXMOX_TARGET_HOST = "botcore"
export PROXMOX_API_STATUS_ENDPOINT = PROXMOX_API + "/api2/json/nodes/botcore/qemu/{vmId}/status/current"
export PROXMOX_API_START_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/botcore/qemu/{vmId}/status/start"
export PROXMOX_API_STOP_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/botcore/qemu/{vmId}/status/stop"
export PROXMOX_API_NEXTID_ENDPOINT = PROXMOX_API + "/api2/json/cluster/nextid"
export PROXMOX_API_CLONE_ENDPOINT = PROXMOX_API + "/api2/extjs/nodes/botcore/qemu/{baseTemplateId}/clone?newid={nextId}\&pool={pool}\&name={name}\&target={targetHost}"

export GFS_NAMESPACE="gfs1"
# export GFS_HOST="192.168.0.160"
export GFS_HOST="192.168.56.60"
export GFS_PORT="5000"
export GFS_USERNAME="root"
export GFS_PASSWORD="root"

export GRAPH_URL="http://$GFS_HOST:$GFS_PORT/api/v1.0/gfs1/graph"
export GRAPH_API_URL="http://$GFS_HOST:$GFS_PORT"

export GRAPHQL_SCHEMA_URL="$GRAPH_API_URL/gfs1/graphql/schema"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
THIS_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
source $THIS_DIR/secrets.sh
