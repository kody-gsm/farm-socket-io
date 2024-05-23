import r_socket
from utils.feedwater import sched
import asyncio
import os

async def main():
    sched.start()

    # internet 연결

    try:
        await r_socket.main()
    except:
        os.system("reboot")


if __name__ == "__main__":
    asyncio.run(main())
