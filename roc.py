# -*- coding: utf-8 -*-

# 特徴の名前と種類を確認
feature_type = []
with open("kddcup.names", "r") as f:
    f.readline()  # ラベル行は読み捨てる
    while True:
        line = f.readline().rstrip()
        if line == "":
            break
        # 特徴名と特徴タイプを切り分けて覚える
        feature_type.append(line.split(": "))

# 答え合わせ用にラベル情報も獲得する
feature_type.append(["label", "symbolic."])

# 最終的に得られるデータ
data = []
with open("kddcup.data.sampled.csv", "r") as f:
    while True:
        line = f.readline().rstrip()
        if line == "":
            break
        features = {}
        for schema, value in zip(feature_type, line.split(",")):
            fname, ftype = schema
            if ftype == 'continuous.':    # 実数値
                features[fname] = float(value)
            elif ftype == 'symbolic.':    # 文字列
                features[fname] = value
            else:
                assert(not "unknown type")
        data.append(features)

print("data ready")

import jubatus
from jubatus.common import Datum

client = jubatus.Anomaly('127.0.0.1', 9199, 'kdd')

true_positive = 0.0
true_negative = 0.0
false_positive = 0.0
false_negative = 0.0


labels = []
scores = []
for datum in data:
    # 答え合わせ用のデータを獲得
    label = datum["label"]

    # ラベル情報を取り除く
    del datum["label"]
    result = client.add(Datum(datum)).score
    scores.append(result)
    if label == 'normal.':
        labels.append(0)
    else:
        labels.append(1)


import json
with open("result.json", "w") as f:
    f.write(json.dumps({"labels": labels, "scores": scores}))
