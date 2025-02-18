import sys
import client
import server
import logger
import BuildInClasses
import QuickValues

log = logger.Logger()

if __name__ == '__main__':
    print("Do not run this file directly")
    log.log("main.py was executed directly", QuickValues.Log.warning)
    log.log(" ".join([str(i) for i in range(100)]), QuickValues.Log.info)
    sys.exit(0)

log.log("Server starting", QuickValues.Log.info)
