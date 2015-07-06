import SimpleHTTPServer
import SocketServer
from itertools import izip


import jubatus
from jubatus.common import Datum

class AnomalyDetect(SimpleHTTPServer.SimpleHTTPRequestHandler):
    allow_reuse_address = True
    def do_GET(self):
        parameters = str(self.headers).rstrip().split("\r\n")
        features = dict(map(lambda x: x.split(": "), parameters))
        features["path"] = self.path

        del features["Cookie"]

        print(features)

        client = jubatus.Anomaly('127.0.0.1', 9199, 'kdd')
        score = client.add(Datum(features)).score

        result = "score: {s}".format(s=score)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(result))
        self.end_headers()
        self.wfile.write(result)

class ReusableTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True

PORT = 8000
httpd = ReusableTCPServer(("", PORT), AnomalyDetect)
print("serving at port", PORT)
httpd.serve_forever()
