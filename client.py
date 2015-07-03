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

import jubatus
from jubatus.common import Datum

client = jubatus.Anomaly('127.0.0.1', 9199, 'kdd')

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

    if label == 'normal.':
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
