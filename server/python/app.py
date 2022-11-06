import asyncio
import websockets
import json

import base64
import cv2 as cv
import numpy as np
import os

from helperClasses.ImageProcessor import ImageProcessor



async def handler(websocket):
    processor = ImageProcessor()

    inc = 0

    async for message in websocket:

        img_binary = base64.b64decode(message)
        #jpg <- binary
        img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
        #raw image <- jpg
        img = cv.imdecode(img_jpg, cv.IMREAD_COLOR)

        if not os.path.exists("./images/{}".format(len(img))):
            os.mkdir("./images/{}".format(len(img)))

        cv.imwrite("./images/{}/{}.jpg".format(len(img),inc), img)
        inc += 1
        print(inc)

        # processor.processMessage(message)
        # processor.displayMask()
        
        # # frame = cv.resize(frame, (640, 480))
        # # encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 65]
        # # man = cv.imencode('.jpg', frame, encode_param)[1]
        # # #sender(man)
        # # await websocket.send(man.tobytes())

        # img_binary = base64.b64decode(message)
        # #jpg <- binary
        # img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
        # #raw image <- jpg
        # img = cv.imdecode(img_jpg, cv.IMREAD_COLOR)

        # # nparr = np.fromstring(message, np.uint8)
        # # # decode image
        # # img = cv.imdecode(nparr, cv.IMREAD_COLOR)
        # cv.imwrite("./testingImgTransfer.png", img)

        # # for player, column, row in [
        # #     ("PLAYER1", 3, 0),
        # #     ("PLAYER2", 3, 1),
        # #     ("PLAYER1", 4, 0),
        # #     ("PLAYER2", 4, 1),
        # #     ("PLAYER1", 2, 0),
        # #     ("PLAYER2", 1, 0),
        # #     ("PLAYER1", 5, 0),
        # # ]:
        # #     event = {
        # #         "type": "play",
        # #         "player": player,
        # #         "column": column,
        # #         "row": row,
        # #     }
        # #     await websocket.send(json.dumps(event))
        # #     await asyncio.sleep(0.5)
        # # event = {
        # #     "type": "win",
        # #     "player": "PLAYER1",
        # # }
        # # await websocket.send(json.dumps(event))
        # # print(message)

async def main():
    print("serving app")
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())