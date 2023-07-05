# @Time: 2023/7/5 11:49
# @Auther: MHC
# @File: tts_saved.py
# @Description:
'''
参考代码
https://github.com/OS984/DiscordBotBackend/blob/3b06b8be39e4dbc07722b0afefeee4c18c136102/NeuralTTS.py
https://github.com/rany2/edge-tts/blob/master/src/edge_tts/communicate.py
'''


import websockets
import asyncio
from datetime import datetime
import time
import re
import uuid
import argparse
import pygame
import io


'''命令行参数解析'''
def parseArgs():
    parser = argparse.ArgumentParser(description='text2speech')
    parser.add_argument('--input', dest='input', help='SSML(语音合成标记语言)的路径', type=str, required=True)
    parser.add_argument('--output', dest='output', help='保存mp3文件的路径', type=str, required=False)
    args = parser.parse_args()
    return args

# Fix the time to match Americanisms
def hr_cr(hr):
    corrected = (hr - 1) % 24
    return str(corrected)

# Add zeros in the right places i.e 22:1:5 -> 22:01:05
def fr(input_string):
    corr = ''
    i = 2 - len(input_string)
    while (i > 0):
        corr += '0'
        i -= 1
    return corr + input_string

# Generate X-Timestamp all correctly formatted
def getXTime():
    now = datetime.now()
    return fr(str(now.year)) + '-' + fr(str(now.month)) + '-' + fr(str(now.day)) + 'T' + fr(hr_cr(int(now.hour))) + ':' + fr(str(now.minute)) + ':' + fr(str(now.second)) + '.' + str(now.microsecond)[:3] + 'Z'

# Async function for actually communicating with the websocket
import websockets
import asyncio
from datetime import datetime
import time
import re
import uuid
import argparse
import pygame
import io

# ...其他函数不变...

# 修改 transferMsTTSData 函数
async def transferMsTTSData(SSML_text):
    req_id = uuid.uuid4().hex.upper()
    print(req_id)
    TRUSTED_CLIENT_TOKEN = "6A5AA1D4EAFF4E9FB37E23D68491D6F4"
    WSS_URL = (
        "wss://speech.platform.bing.com/consumer/speech/synthesize/"
        + "readaloud/edge/v1?TrustedClientToken="
        + TRUSTED_CLIENT_TOKEN
    )
    endpoint2 = f"{WSS_URL}&ConnectionId={req_id}"
    async with websockets.connect(endpoint2,extra_headers={
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Origin": "chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41"}) as websocket:
        # ...省略了发送消息的部分...

        message_1 = (
            f"X-Timestamp:{getXTime}\r\n"
            "Content-Type:application/json;charset=utf-8\r\n"
            "Path:speech.config\r\n\r\n"
            '{"context":{"synthesis":{"audio":{"metadataOptions":{"sentenceBoundaryEnabled":false,"wordBoundaryEnabled":true},'
            '"outputFormat":"audio-24khz-48kbitrate-mono-mp3"'"}}}}\r\n")
        await websocket.send(message_1)
        message_2 = (
            f"X-RequestId:{req_id}\r\n"
            "Content-Type:application/ssml+xml\r\n"
            f"X-Timestamp:{getXTime()}Z\r\n"  # This is not a mistake, Microsoft Edge bug.
            "Path:ssml\r\n\r\n"
            f"{SSML_text}")
        await websocket.send(message_2)

        # Checks for close connection message
        end_resp_pat = re.compile('Path:turn.end')

        audio_stream = b''
        while(True):
            response = await websocket.recv()
            print('receiving...')
            if (re.search(end_resp_pat, str(response)) == None):
                if type(response) == type(bytes()):
                    try:
                        needle = b'Path:audio\r\n'
                        start_ind = response.find(needle) + len(needle)
                        audio_stream += response[start_ind:]
                    except:
                        pass
            else:
                break

        return audio_stream  # 返回音频数据

# 修改 mainSeq 函数
async def mainSeq(SSML_text):
    audio_stream = await transferMsTTSData(SSML_text)

    pygame.init()
    pygame.mixer.init()
    audio_file = io.BytesIO(audio_stream)
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def get_SSML(path):
    with open(path,'r',encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    args = parseArgs()
    SSML_text = get_SSML(args.input)
    asyncio.get_event_loop().run_until_complete(mainSeq(SSML_text))
    print('completed')

