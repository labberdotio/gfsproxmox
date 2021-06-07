# ENV Vars which are set by the start script, generally this mimics cloud native 
#   as ENV vars are passed into container orchestrators as settings too or in vault etc.  

export TEST_TEMPLATE_TYPE=""
export TEST_INSTANCE_TYPE=""

export GFS_NAMESPACE="gfs1"
# export GFS_HOST="192.168.0.160"
export GFS_HOST="192.168.0.160"
export GFS_PORT="5000"
export GFS_USERNAME="root"
export GFS_PASSWORD="root"

export PMOXAPI_HOST="192.168.0.180"
export PMOXAPI_PORT=8006

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
