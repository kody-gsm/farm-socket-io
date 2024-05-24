import r_socket
from utils.feedwater import sched
import asyncio
import os
import time

async def main():
    sched.start()

    # internet 연결

    #try:
    await r_socket.main()
    #except Exception as e:
     #   print(e)
        # time.sleep(10)
        # os.system("reboot")


if __name__ == "__main__":
    asyncio.run(main())

