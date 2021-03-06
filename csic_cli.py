# -*- coding: utf-8 -*-

target = "output_http_csic_2010_weka_with_duplications_utf8_escd_v02_full.csv"

data = []
with open(target, "r") as f:
    schema = f.readline().rstrip().replace("\"", "").split(",")
    while True:
        line = f.readline()
        if not line:
            break

        row = line.rstrip().replace("\"", "").split(",")
        datum = {}
        for key, value in zip(schema, row):
            datum[key] = value
        data.append(datum)

import jubatus
from jubatus.common import Datum

client = jubatus.Anomaly('127.0.0.1', 9199, 'csic')

true_positive = 0.0
true_negative = 0.0
false_positive = 0.0
false_negative = 0.0

for datum in data:
    # 答え合わせ用のデータを獲得
    label = datum["label"]

    # ラベル情報を取り除く
    del datum["label"]
    result = client.add(Datum(datum)).score

    # 1.5以上なら異常とみなすこととする
    is_anomaly = 1.5 < result

    if label == 'norm':
        # 教師データ中で正常とされる物
        if is_anomaly:
            # Jubatusが間違えて異常とみなした
            false_positive += 1
        else:
            # Jubatusが正しく正常とみなした
            true_positive += 1
    else:
        # 教師データ中で異常とされる物
        if is_anomaly:
            # Jubatusが正しく異常とみなした
            true_negative += 1
        else:
            # Jubatusが間違えて正常とみなした
            false_negative += 1

# それぞれの公式に当てはめてF値を算出
precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
f_measure = 2 * recall * precision / (recall + precision)

print("precision: {p}, recall: {r}, f_measure: {f}".format(p=precision, r=recall, f=f_measure))
