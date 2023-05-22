# -*- coding: utf-8 -*-
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

# パラメータ
a = 0.60

# 音程(log(f2/f1))の底
b = pow(2, 1.0/12.0)

# dB値振幅変換
def db2amp(db, p0):
    return 10 ** (db / 20) * p0

# テンション算出
def tension_partial(f1, f2, f3, a1, a2, a3):
    return a1 * a2 * a3 * math.exp((-1) * (((math.log(f3 / f2, b) - math.log(f2 / f1, b)) / a) ** 2))
  
# csv読み込み
csv_freq = open("./sn_freq.csv", "r")
csv_dB = open("./sn_dB.csv", "r")

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

# root      : 最低音
# second    : 二音目
# base      : 調
# ind       : 三音目(最低音の1オクターブ上まで動かす)
# i         : 最低音の倍音のためのindex(~5)、最低音のi倍音まで計算に利用する
# j         : 二音目の倍音のためのindex(~5)、二音目のj倍音まで計算に利用する
# k         : 三音目の倍音のためのindex(~5)、三音目のk倍音まで計算に利用する

# C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B
# 0, 1 , 2, 3 , 4, 5, 6 , 7, 8 , 9, 10, 11

# ルート変化------------------------------------------------
# root = 0
# second = 4
# third = second + 3
# forth = 13 - third + root
# base_range = 12
# ten_list = [[] for _ in range(base_range)]


# for base in range(0,base_range):
#     for ind in range(0, forth):
#         t_par = 0
#         for i in range(0, 6):
#             for j in range(0, 6):
#                 for k in range(0, 6):
#                     for l in range(0, 6):
#                         partial1_amp = "F" + str(i) + "_amp[" + str(root + base) + "]"
#                         partial2_amp = "F" + str(j) + "_amp[" + str(second + base) + "]"
#                         partial3_amp = "F" + str(k) + "_amp[" + str(third + base) + "]"
#                         partial4_amp = "F" + str(l) + "_amp[" + str(ind + third + base) + "]"

#                         partial1_freq = "F" + str(i) + "_freq[" + str(root + base) + "]"
#                         partial2_freq = "F" + str(j) + "_freq[" + str(second + base) + "]"
#                         partial3_freq = "F" + str(k) + "_freq[" + str(third + base) + "]"
#                         partial4_freq = "F" + str(l) + "_freq[" + str(ind + third + base) + "]"

#                         # リスト化
#                         partials_freq = [float(eval(partial1_freq)), float(eval(partial2_freq)), float(eval(partial3_freq)), float(eval(partial4_freq))]
#                         partials_amp = [float(eval(partial1_amp)), float(eval(partial2_amp)), float(eval(partial3_amp)), float(eval(partial4_amp))]

#                         # 3音選出して計算
#                         # 4C3 なので4通り
#                         sorted_freq = [partials_freq[0], partials_freq[1], partials_freq[2]]
#                         sorted_amp = [partials_amp[0], partials_amp[1], partials_amp[2]]
#                         sorted_freq.sort()
#                         t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], sorted_amp[0], sorted_amp[1], sorted_amp[2])

#                         sorted_freq = [partials_freq[0], partials_freq[1], partials_freq[3]]
#                         sorted_amp = [partials_amp[0], partials_amp[1], partials_amp[3]]
#                         sorted_freq.sort()
#                         t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], sorted_amp[0], sorted_amp[1], sorted_amp[2])
                        
#                         sorted_freq = [partials_freq[0], partials_freq[2], partials_freq[3]]
#                         sorted_amp = [partials_amp[0], partials_amp[2], partials_amp[3]]
#                         sorted_freq.sort()
#                         t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], sorted_amp[0], sorted_amp[1], sorted_amp[2])

#                         sorted_freq = [partials_freq[1], partials_freq[2], partials_freq[3]]
#                         sorted_amp = [partials_amp[1], partials_amp[2], partials_amp[3]]
#                         sorted_freq.sort()
#                         t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], sorted_amp[0], sorted_amp[1], sorted_amp[2])

#         ten_list[base].append(t_par)

# # CSV出力
# # f = open('out.csv', 'w')
# # writer = csv.writer(f)
# # writer.writerows(ten_list)
# # f.close()


# # グラフ
# fig, ax = plt.subplots()

# # x軸用
# t = np.linspace(0, forth-1, forth)

# # 色、ラベル名用のリスト
# c = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#ff0000', '#00ff00', '#0000ff', '#000000']
# l = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# # x, y軸ラベル、グラフタイトル
# ax.set_xlabel('third interval(semitone)')
# ax.set_ylabel('tension')
# ax.set_title(r'Tension')

# figsize=(6.4, 4.8/0.96)

# # スケールを揃える
# # ax.set_aspect('equal')

# ax.grid()            # 罫線
# #ax.set_xlim([-10, 10]) # x方向の描画範囲を指定
# # ax.set_ylim([0, 5])    # y方向の描画範囲を指定

# for i in range(base_range):
#     ax.plot(t, ten_list[i], color=c[i], label=l[i])
 
# # 凡例
# ax.legend(loc=0)   

# # レイアウトの設定
# fig.tight_layout()

# # plt.savefig('hoge.png') # 画像の保存

# plt.show()
# ---------------------------------------------------------

# n倍音まで使用----------------------------------------------
root = 0
second = 4
third = second + 3
forth = 13 - third + root
overtone_range = 6
ten_list = [[] for _ in range(overtone_range)]


for o_r in range(0, overtone_range):
    for ind in range(0, forth):
        t_par = 0
        for i in range(0, o_r+1):
            for j in range(0, o_r+1):
                for k in range(0, o_r+1):
                    for l in range(0, o_r+1):
                        partial1_amp = "F" + str(i) + "_amp[" + str(root) + "]"
                        partial2_amp = "F" + str(j) + "_amp[" + str(second) + "]"
                        partial3_amp = "F" + str(k) + "_amp[" + str(third) + "]"
                        partial4_amp = "F" + str(l) + "_amp[" + str(ind + third) + "]"

                        partial1_freq = "F" + str(i) + "_freq[" + str(root) + "]"
                        partial2_freq = "F" + str(j) + "_freq[" + str(second) + "]"
                        partial3_freq = "F" + str(k) + "_freq[" + str(third) + "]"
                        partial4_freq = "F" + str(l) + "_freq[" + str(ind + third) + "]"

                        # リスト化
                        partials_freq = [float(eval(partial1_freq)), float(eval(partial2_freq)), float(eval(partial3_freq)), float(eval(partial4_freq))]
                        partials_amp = [float(eval(partial1_amp)), float(eval(partial2_amp)), float(eval(partial3_amp)), float(eval(partial4_amp))]

                        # 3音選出して計算
                        # 4C3 なので4通り
                        sorted_freq = [partials_freq[0], partials_freq[1], partials_freq[2]]
                        sorted_amp = [partials_amp[0], partials_amp[1], partials_amp[2]]
                        sorted_freq.sort()
                        t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], sorted_amp[0], sorted_amp[1], sorted_amp[2])

                        sorted_freq = [partials_freq[0], partials_freq[1], partials_freq[3]]
                        sorted_amp = [partials_amp[0], partials_amp[1], partials_amp[3]]
                        sorted_freq.sort()
                        t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], sorted_amp[0], sorted_amp[1], sorted_amp[2])
                        
                        sorted_freq = [partials_freq[0], partials_freq[2], partials_freq[3]]
                        sorted_amp = [partials_amp[0], partials_amp[2], partials_amp[3]]
                        sorted_freq.sort()
                        t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], sorted_amp[0], sorted_amp[1], sorted_amp[2])

                        sorted_freq = [partials_freq[1], partials_freq[2], partials_freq[3]]
                        sorted_amp = [partials_amp[1], partials_amp[2], partials_amp[3]]
                        sorted_freq.sort()
                        t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], sorted_amp[0], sorted_amp[1], sorted_amp[2])

        ten_list[o_r].append(t_par/4)

# CSV出力
# f = open('out.csv', 'w')
# writer = csv.writer(f)
# writer.writerows(ten_list)
# f.close()


# グラフ
fig, ax = plt.subplots()

# 書き込み
y_max = 0.06
font_dict = dict(size=20)
bbox_dict = dict(edgecolor="#000000",
                 facecolor="#ffffff",
                 fill=True)
ax.text(0.2, y_max * 0.85, "1st interval = 4.0\n2nd interval = 3.0", bbox=bbox_dict, fontdict=font_dict)

# x軸用
t = np.linspace(0, forth-1, forth)

# 色、ラベル名，マーカー用のリスト
c = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#a65628', '#ffff33', '#f781bf', '#ff0000', '#00ff00', '#0000ff', '#000000']
l = ["F0 only", "F0, F1", "F0 - F2", "F0 - F3", "F0 - F4", "F0 - F5"]
m = [".", ",", "^", "p", "*", "D"]

# x, y軸ラベル、グラフタイトル
ax.set_xlabel('3rd interval(semitone)', fontsize = 25)
ax.set_ylabel('tension', fontsize = 25)
# ax.set_title(r'Tension')

# 軸の数字の文字サイズ
plt.tick_params(labelsize = 20)

figsize=(6.4, 4.8/0.96)

# スケールを揃える
# ax.set_aspect('equal')

ax.grid()            # 罫線
#ax.set_xlim([-10, 10]) # x方向の描画範囲を指定
ax.set_ylim([0, y_max])    # y方向の描画範囲を指定

for i in range(overtone_range):
    ax.plot(t, ten_list[i], color=c[i], label=l[i], linestyle="dashed", marker=m[i], markersize = 10)
 
# 凡例
ax.legend(loc=0)   

# レイアウトの設定
fig.tight_layout()

# plt.savefig('hoge.png') # 画像の保存

plt.show()

