# -*- coding: utf-8 -*-
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

# パラメータ
a = 0.60
beta1 = 0.80
beta2 = 1.60
beta3 = 4.00
gamma = 1.250
sigma = 0.207

# 色、ラベル名用のリスト
c = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#ff0000', '#00ff00', '#0000ff', '#000000']
label = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]


# 音程(log(f2/f1))の底
b = pow(2, 1.0/12.0)

# dB値振幅変換
def db2amp(db, p0):
    return 10 ** (db / 20) * p0

# テンション算出
def tension_partial(f1, f2, f3, a1, a2, a3):
    return a1 * a2 * a3 * math.exp((-1) * (((math.log(f3 / f2, b) - math.log(f2 / f1, b)) / a) ** 2))

def dissonance_partial(f1, f2, a1, a2):
    return  a1 * a2 * beta3 * (math.exp((-1) * beta1 * math.log(f2 / f1, b) ** gamma) - math.exp((-1) * beta2 * math.log(f2 / f1, b) ** gamma))

# csv読み込み
csv_freq = open("./pianoC2A6_freq.csv", "r")
csv_dB = open("./pianoC2A6_dB.csv", "r")

# 行リスト
freq_list = csv.reader(csv_freq, delimiter = ",", doublequote = True, lineterminator = "\r\n", quotechar = '"', skipinitialspace = True)
dB_list = csv.reader(csv_dB, delimiter = ",", doublequote = True, lineterminator = "\r\n", quotechar = '"', skipinitialspace = True)

# 列リストに変換
F0_freq = []
F1_freq = []
F2_freq = []
F3_freq = []
F4_freq = []
F5_freq = []
F0_amp = []
F1_amp = []
F2_amp = []
F3_amp = []
F4_amp = []
F5_amp = []


header_freq = next(freq_list)
for row in freq_list:
    F0_freq.append(row[1])
    F1_freq.append(row[2])
    F2_freq.append(row[3])
    F3_freq.append(row[4])
    F4_freq.append(row[5])
    F5_freq.append(row[6])

header_dB = next(dB_list)
# p_0 = 20e-6
p_0 = 1
for row in dB_list:
    F0_amp.append(db2amp(float(row[1]), p_0))
    F1_amp.append(db2amp(float(row[2]), p_0))
    F2_amp.append(db2amp(float(row[3]), p_0))
    F3_amp.append(db2amp(float(row[4]), p_0))
    F4_amp.append(db2amp(float(row[5]), p_0))
    F5_amp.append(db2amp(float(row[6]), p_0))


# ----------------------------------------------------------
# root          : 最低音
# second        : 二音目
# third         : 三音目のとりうる一番高い音
# base_range    : 最低音の動かす範囲（半音数）（root = 0, base_range = 12のときC4~B4）
# ind           : 三音目をthirdまで動かす
# i             : 最低音の倍音のためのindex。F5まで計算に利用する
# j             : 二音目の倍音のためのindex。F5まで計算に利用する
# k             : 三音目の倍音のためのindex。F5まで計算に利用する
# dis_list      : 不協和度。最低音ごとに格納
# ten_list      : 緊張度。最低音ごとに格納
# ins_list      : 不安定度。最低音ごとに格納
# ----------------------------------------------------------
# C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B
# 0, 1 , 2, 3 , 4, 5, 6 , 7, 8 , 9, 10, 11

root = 0
second = 4
third = 13 - second + root
base_range = 12
dis_list = [[] for _ in range(base_range)]


for base in range(0,base_range):
    for ind in range(0, third):
        d_par = 0
        for i in range(0, 6):
            for j in range(0, 6):
                for k in range(0, 6):
                    partial1_amp = "F" + str(i) + "_amp[" + str(root + base) + "]"
                    partial2_amp = "F" + str(j) + "_amp[" + str(second + base) + "]"
                    partial3_amp = "F" + str(k) + "_amp[" + str(ind + second + base) + "]"
                    partial1_freq = "F" + str(i) + "_freq[" + str(root + base) + "]"
                    partial2_freq = "F" + str(j) + "_freq[" + str(second + base) + "]"
                    partial3_freq = "F" + str(k) + "_freq[" + str(ind + second + base) + "]"

                     # リスト化
                    partials_freq = [float(eval(partial1_freq)), float(eval(partial2_freq)), float(eval(partial3_freq))]
                    partials_amp = [float(eval(partial1_amp)), float(eval(partial2_amp)), float(eval(partial3_amp))]

                    # 2音選出して計算
                    # 3C2 なので3通り
                    sorted_freq = [partials_freq[0], partials_freq[1]]
                    sorted_amp = [partials_amp[0], partials_amp[1]]
                    sorted_freq.sort()
                    d_par += dissonance_partial(sorted_freq[0], sorted_freq[1], sorted_amp[0], sorted_amp[1])

                    sorted_freq = [partials_freq[0], partials_freq[2]]
                    sorted_amp = [partials_amp[0], partials_amp[2]]
                    sorted_freq.sort()
                    d_par += dissonance_partial(sorted_freq[0], sorted_freq[1], sorted_amp[0], sorted_amp[1])

                    sorted_freq = [partials_freq[1], partials_freq[2]]
                    sorted_amp = [partials_amp[1], partials_amp[2]]
                    sorted_freq.sort()
                    d_par += dissonance_partial(sorted_freq[0], sorted_freq[1], sorted_amp[0], sorted_amp[1])


        dis_list[base].append(d_par / 3)

ten_list = [[] for _ in range(base_range)]


for base in range(0,base_range):
    for ind in range(0, third):
        t_par = 0
        for i in range(0, 6):
            for j in range(0, 6):
                for k in range(0, 6):
                    partial1_amp = "F" + str(i) + "_amp[" + str(root + base) + "]"
                    partial2_amp = "F" + str(j) + "_amp[" + str(second + base) + "]"
                    partial3_amp = "F" + str(k) + "_amp[" + str(ind + second + base) + "]"
                    partial1_freq = "F" + str(i) + "_freq[" + str(root + base) + "]"
                    partial2_freq = "F" + str(j) + "_freq[" + str(second + base) + "]"
                    partial3_freq = "F" + str(k) + "_freq[" + str(ind + second + base) + "]"

                    # 選んだ3音を小さい順にソート
                    # 音量(振幅)は積を使うだけなのでそのまま
                    sorted_freq = [float(eval(partial1_freq)), float(eval(partial2_freq)), float(eval(partial3_freq))]
                    sorted_freq.sort()

                    t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], float(eval(partial1_amp)), float(eval(partial2_amp)), float(eval(partial3_amp)))
        ten_list[base].append(t_par)


# tesion, dissonance加算してinstbility算出
ins_list = [[] for _ in range(base_range)]
ins_list_op = []

for i1 in range(0, base_range):
    for i2 in range(0, third):
        ins_list[i1].append(dis_list[i1][i2] + sigma * ten_list[i1][i2])

# for i in range(base_range):
#     ins_list_op.append([label[i]+"-min1stinv", ins_list[i][5]])


# CSV出力
# f = open('out.csv', 'w')
# writer = csv.writer(f)
# writer.writerows(ins_list)
# f.close()


# グラフ
fig, ax = plt.subplots()

# x軸用
t = np.linspace(0, third-1, third)

# x, y軸ラベル、グラフタイトル
ax.set_xlabel('second interval(semitone)')
ax.set_ylabel('instability')
ax.set_title(r'Instability')

figsize=(6.4, 4.8/0.96)

# スケールを揃える
# ax.set_aspect('equal')

ax.grid()            # 罫線
#ax.set_xlim([-10, 10]) # x方向の描画範囲を指定
# ax.set_ylim([0, 5])    # y方向の描画範囲を指定

for i in range(base_range):
    ax.plot(t, ins_list[i], color=c[i], label=label[i])
 
# 凡例
ax.legend(loc=0)   

# レイアウトの設定
fig.tight_layout()

# plt.savefig('hoge.png') # 画像の保存

plt.show()

# ---------------------------------------------------
