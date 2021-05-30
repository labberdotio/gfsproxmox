
import logging

# logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

from gfsgql import GFSGQL

# 
# Main
# 
if __name__ == '__main__':

    gfs_host = "localhost"
    gfs_port = "5000"
    gfs_username = None
    gfs_password = None

    gqlClient = GFSGQL(
        gfs_host = gfs_host,
        gfs_port = gfs_port,
        gfs_username = gfs_username,
        gfs_password = gfs_password,
    )

    gqlClient.gqlexec(
        """
            mutation updateIp($id:String!, $name:String, $address:String, ) {
                updateIp(id:$id, name:$name, address:$address, ) {
                    instance {
                        id, name, address,
                    },
                    ok
                }
            }
        """,
        {
            "id": "5202",
            "name": "myname",
            "address": "myaddress"
        }
    )

