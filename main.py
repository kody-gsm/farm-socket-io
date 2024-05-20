import r_socket
from utils.feedwater import sched
import asyncio

async def main():
    sched.start()

    # internet 연결

    try:
        r_socket.main()
    except:
        pass # reboot


if __name__ == "__main__":
    asyncio.run(main())
