# ENV Vars which are set by the start script, generally this mimics cloud native 
#   as ENV vars are passed into container orchestrators as settings too or in vault etc.  

export TEST_TEMPLATE_TYPE=""
export TEST_INSTANCE_TYPE=""

##################################
## proxmodNodeListener
#### @TODO - implement properly mapped node -> IP discovery
export PROXMOX_API_HOST='192.168.0.181'
export PROXMOX_API_PORT='8006'
export PROXMOX_POOL="botcanics"
export PROXMOX_TARGET_HOST="botcore"
export PROXMOX_API_TOKEN_ID="root@pam!admin"
export PROXMOX_API_TOKEN_SECRET="b41e99ed-7902-4daf-9530-d3aaa7fc3954"
# for the 'gfs' proxmox host
# export PROXMOX_API_TOKEN_ID="root@pam!admin"
# export PROXMOX_API_TOKEN_SECRET="051a3faf-b795-4141-8fc6-0d49606d06f4"
export PROXMOX_NODE_LISTENER_LISTENERADDR="0.0.0.0"
export PROXMOX_NODE_LISTENER_LISTENERPORT="5010"

##################################
## GFS
export GFS_NAMESPACE="gfs1"
export GFSAPI_HOST="192.168.0.160"
export GFSAPI_PORT="5000"
export GFSAPI_USERNAME="root"
export GFSAPI_PASSWORD="root"
export GFS_NAMESPACE="$GFSAPI_HOST"
export GFS_HOST="$GFSAPI_HOST"
export GFS_PORT="$GFSAPI_PORT"
export GFS_USERNAME="$GFSAPI_USERNAME"
export GFS_PASSWORD="$GFSAPI_PASSWORD"
export GRAPH_URL="http://$GFSAPI_HOST:$GFSAPI_PORT/api/v1.0/gfs1/graph"
export GRAPH_API_URL="http://$GFSAPI_HOST:$GFSAPI_PORT"
export GRAPHQL_SCHEMA_URL="$GRAPH_API_URL/gfs1/graphql/schema"

##################################
## TrueNAS
export TRUENAS_USER="root"
export TRUENAS_PASSWORD="root123"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
_THIS_SETTINGS_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
# source $THIS_DIR/secrets.sh
