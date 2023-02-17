import asyncio
import websockets
from multiprocessing import Process
from barabasz.utils import process_message
import os
import sys


def main():
    while True:

        async def listen_to_websocket():
            async with websockets.connect(
                os.getenv("SIGNAL_WEBSOCKET_RX_ENDPOINT")
            ) as websocket:
                while True:
                    try:
                        message = await websocket.recv()
                        p = Process(target=process_message, args=[message])
                        p.run()

                    except KeyError as err:
                        print(
                            f"ERROR processing message: {message} \n {str(err)}",
                            file=sys.stderr,
                        )

        try:
            asyncio.run(listen_to_websocket())
        except websockets.exceptions.ConnectionClosedError as err:
            print(f"Connection broken, restarting...\n {str(err)}", file=sys.stderr)


if __name__ == "__main__":
    main()
