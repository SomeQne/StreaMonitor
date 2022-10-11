import json
from threading import Thread
from websocket import create_connection, WebSocketConnectionClosedException, WebSocketException
from contextlib import closing


def getVideoWSSVR(self, url, filename):
    self.stopDownloadFlag = False

    def execute():
        try:
            with closing(create_connection(url, timeout=10)) as conn:
                conn.send('{"url":"stream/hello","version":"0.0.1"}')
                while not self.stopDownloadFlag:
                    t = conn.recv()
                    try:
                        tj = json.loads(t)
                        if 'url' in tj:
                            if tj['url'] == 'stream/qual':
                                conn.send('{"quality":"test","url":"stream/play","version":"0.0.1"}')
                                break
                        if 'message' in tj:
                            if tj['message'] == 'ping':
                                return False
                    except:
                        return False

                with open(filename, 'wb') as outfile:
                    while not self.stopDownloadFlag:
                        outfile.write(conn.recv())
        except WebSocketConnectionClosedException:
            self.log('Show ended (WebSocket connection closed)')
            return True
        except WebSocketException:
            return False

    def terminate():
        self.stopDownloadFlag = True

    process = Thread(target=execute)
    process.start()
    self.stopDownload = terminate
    process.join()
    self.stopDownload = None
    return True