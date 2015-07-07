# -*- coding: utf-8 -*-
import socket
import msgpack
from contextlib import closing

import jubatus
from jubatus.common import Datum

from io import BytesIO

host = '127.0.0.1'
port = 9191
backlog = 10
bufsize = 4096

# listenするソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with closing(sock):
    sock.bind((host, port))
    sock.listen(backlog)
    buf = BytesIO()
    while True:
        # Connectされるのを待つ
        conn, _ = sock.accept()

        # 届いたデータを全て読んだ後ソケットを閉じる
        buf = BytesIO()
        while True:
            msg = conn.recv(bufsize)
            if len(msg) == 0:
                break
            buf.write(msg)
        conn.close()

        # 届いたデータをMessagePackからデシリアライズする
        buf.seek(0)
        tuple_array = msgpack.Unpacker(buf)

        # Jubatusに接続
        client = jubatus.Anomaly('127.0.0.1', 9199, 'kdd')

        # Fluentdからのメッセージは複数のタプルを含んでいる
        # [name, string(シリアライズされたデータ)]
        # nameに相当する部分は今回は使わないので無視
        for _, payload in tuple_array:
            multi_msg = BytesIO()
            multi_msg.write(payload)

            try:
                # シリアライズされたデータを読み出す
                multi_msg.seek(0)
                multi_tuple = msgpack.Unpacker(multi_msg)

                # シリアライズされたデータは複数の[time, record]を含む
                for time, record in multi_tuple:

                    # Jubatusに与えたいデータだけを選択する
                    features = {}
                    features['path'] = record['path']
                    features['method'] = record['method']
                    features['referer'] = record['referer'] or ""

                    # Jubatusに与えて異常度を測定
                    score = client.add(Datum(features)).score
                    print("{f} => {s}".format(f=features, s=score))

            except Exception as e:
                # 例外は今回は表示だけして無視
                print(e)
                pass

