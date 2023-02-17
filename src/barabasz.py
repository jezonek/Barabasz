import logging
import asyncio
import websockets
from multiprocessing import Process, Manager
from barabasz.utils import process_message
import os
import sys


async def listen_to_websocket():
    async with websockets.connect(
        os.getenv("SIGNAL_WEBSOCKET_RX_ENDPOINT")
    ) as websocket:
        with Manager() as conversation_manager:
            conversation_dict = conversation_manager.dict()
            conversation_dict = {}
            while True:
                try:
                    message = await websocket.recv()
                    # process_message(conversation_dict, message)
                    p = Process(
                        target=process_message, args=[conversation_dict, message]
                    )
                    p.run()

                except KeyError as err:
                    print(
                        f"ERROR processing message: {message} \n {str(err)}",
                        file=sys.stderr,
                    )


def main():
    while True:
        try:
            asyncio.run(listen_to_websocket())
        except websockets.exceptions.ConnectionClosedError as err:
            print(f"Connection broken, restarting...\n {str(err)}", file=sys.stderr)


if __name__ == "__main__":
    main()
