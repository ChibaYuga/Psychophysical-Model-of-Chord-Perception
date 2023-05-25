# -*- coding: utf-8 -*-
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

# パラメータ
beta1 = 0.80
beta2 = 1.60
beta3 = 4.00
gamma = 1.250
a = 0.60
e = 1.558
sigma = 0.207

# 音程(log(f2/f1))の底
b = pow(2, 1.0/12.0)



# 音データの読み込み--------------------------------------------------------------
# 倍音を含めた周波数とdB値のcsvファイルからモデル算出用に整形
# Fn_freq：基音・倍音の周波数のリスト
# Fn_amp：基音・倍音の振幅（大きさ）のリスト

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

# dB値振幅変換
def db2amp(db, p0):
    return 10 ** (db / 20) * p0

p_0 = 1
for row in dB_list:
    F0_amp.append(db2amp(float(row[1]), p_0))
    F1_amp.append(db2amp(float(row[2]), p_0))
    F2_amp.append(db2amp(float(row[3]), p_0))
    F3_amp.append(db2amp(float(row[4]), p_0))
    F4_amp.append(db2amp(float(row[5]), p_0))
    F5_amp.append(db2amp(float(row[6]), p_0))

# -----------------------------------------------------------------------------


def main():
    root = 0
    second = 4
    third = second + 3
    forth = 13 -third + root
    overtone_range = 6

    # tension_tri = ten_tri(root, second, third, overtone_range)
    # print(tension_tri)


    # tension_tet = ten_tet(0, 4, 7, 11, overtone_range)
    # print("tension of CM7 : " +str(tension_tet))

    

    ins_list =[]
    for i in range(0,forth):
        ins_list.append(ins_tet(root, second, third, third + i, overtone_range))

    # dissonance_tri = dis_tri(root, second, third, overtone_range)
    # print(ten_list)
    
    # グラフ
    fig, ax = plt.subplots()
    t = np.linspace(0, forth-1, forth)

    ax.set_xlabel('third interval(semitone)')
    ax.set_ylabel('Instability')
    ax.set_title(r'I')

    figsize=(6.4, 4.8/0.96)

    ax.grid()
    ax.plot(t, ins_list)

    # 凡例
    ax.legend(loc=0)   

    # レイアウトの設定
    fig.tight_layout()

    plt.show()  

    # # グラフ
    # fig, ax = plt.subplots()
    # t = np.linspace(0, forth-1, forth)

    # ax.set_xlabel('3rd interval(semitone)')
    # ax.set_ylabel('dissonance')
    # ax.set_title(r'Dissonance')

    # figsize=(6.4, 4.8/0.96)

    # ax.grid()
    # ax.plot(t, dis_list)

    # # 凡例
    # ax.legend(loc=0)   

    # # レイアウトの設定
    # fig.tight_layout()

    # plt.show()  

    return

# root      : 最低音
# second    : 二音目
# base      : 調
# ind       : 三音目(最低音の1オクターブ上まで動かす)
# i         : 最低音の倍音のためのindex(~5)、最低音のi倍音まで計算に利用する
# j         : 二音目の倍音のためのindex(~5)、二音目のj倍音まで計算に利用する
# k         : 三音目の倍音のためのindex(~5)、三音目のk倍音まで計算に利用する

# C4, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B  ~C
# 0, 1 , 2, 3 , 4, 5, 6 , 7, 8 , 9, 10, 11 ~24









# Dissonance caliculation
def dissonance_partial(f1, f2, a1, a2):
    return  a1 * a2 * beta3 * (math.exp((-1) * beta1 * math.log(f2 / f1, b) ** gamma) - math.exp((-1) * beta2 * math.log(f2 / f1, b) ** gamma))

# 2 tones Dissonance
def dis_bi(root, second, overtone_range):
    dis_list = [[] for _ in range(overtone_range)]

    for o_r in range(0,overtone_range):
        d_par = 0
        for i in range(0, o_r+1):
            for j in range(0, o_r+1):
                partial1_amp = "F" + str(i) + "_amp[" + str(root) + "]"
                partial2_amp = "F" + str(j) + "_amp[" + str(second) + "]"
                partial1_freq = "F" + str(i) + "_freq[" + str(root) + "]"
                partial2_freq = "F" + str(j) + "_freq[" + str(second) + "]"

                # 選んだ2音を小さい順にソート
                # 音量(振幅)は積を使うだけなのでそのまま
                sorted_freq = [float(eval(partial1_freq)), float(eval(partial2_freq))]
                sorted_freq.sort()

                d_par += dissonance_partial(sorted_freq[0], sorted_freq[1], float(eval(partial1_amp)), float(eval(partial2_amp)))
    
    return d_par

# 3 tones Dissonance
def dis_tri(root, second, third, overtone_range):
    return (dis_bi(root, second, overtone_range) + dis_bi(second, third, overtone_range) + dis_bi(root, third, overtone_range)) / 3

# 4 tones Dissonance
def dis_tet(root, second, third, forth, overtone_range):
    return (dis_bi(root, second, overtone_range) + dis_bi(root, third, overtone_range) + dis_bi(root, forth, overtone_range) + dis_bi(second, third, overtone_range) + dis_bi(second, forth, overtone_range) + dis_bi(third, forth, overtone_range)) / 6

# Tension caliculation
def tension_partial(f1, f2, f3, a1, a2, a3):
    return a1 * a2 * a3 * math.exp((-1) * (((math.log(f3 / f2, b) - math.log(f2 / f1, b)) / a) ** 2))
  
# 3 tones Tension
def ten_tri(root, second, third, overtone_range):
    for o_r in range(0, overtone_range):
        t_par = 0
        for i in range(0, o_r+1):
            for j in range(0, o_r+1):
                for k in range(0, o_r+1):
                    partial1_amp = "F" + str(i) + "_amp[" + str(root) + "]"
                    partial2_amp = "F" + str(j) + "_amp[" + str(second) + "]"
                    partial3_amp = "F" + str(k) + "_amp[" + str(third) + "]"
                    partial1_freq = "F" + str(i) + "_freq[" + str(root) + "]"
                    partial2_freq = "F" + str(j) + "_freq[" + str(second) + "]"
                    partial3_freq = "F" + str(k) + "_freq[" + str(third) + "]"

                    # 選んだ3音を小さい順にソート
                    # 音量(振幅)は積を使うだけなのでそのまま
                    sorted_freq = [float(eval(partial1_freq)), float(eval(partial2_freq)), float(eval(partial3_freq))]
                    sorted_freq.sort()

                    t_par += tension_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], float(eval(partial1_amp)), float(eval(partial2_amp)), float(eval(partial3_amp)))
    return t_par

# 4 tones Tension
def ten_tet(root, second, third, forth, overtone_range):
    return (ten_tri(root, second, third, overtone_range) + ten_tri(root, second, forth, overtone_range) + ten_tri(root, third, forth, overtone_range) + ten_tri(second, third, forth, overtone_range)) / 4

# Modality caliculation
def modality_partial(f1, f2, f3, a1, a2, a3):
    return (-1) * a1 * a2 * a3 * (2 * (math.log(f3 / f2, b) - math.log(f2 / f1, b)) / e) * math.exp((1) * ((-1) * ((math.log(f3 / f2, b) - math.log(f2 / f1, b))) ** 4) / 4)

# 3 tones Modality
def mod_tri(root, second, third, overtone_range):
    for o_r in range(0, overtone_range):
        m_par = 0
        for i in range(0, o_r+1):
            for j in range(0, o_r+1):
                for k in range(0, o_r+1):
                    partial1_amp = "F" + str(i) + "_amp[" + str(root) + "]"
                    partial2_amp = "F" + str(j) + "_amp[" + str(second) + "]"
                    partial3_amp = "F" + str(k) + "_amp[" + str(third) + "]"
                    partial1_freq = "F" + str(i) + "_freq[" + str(root) + "]"
                    partial2_freq = "F" + str(j) + "_freq[" + str(second) + "]"
                    partial3_freq = "F" + str(k) + "_freq[" + str(third) + "]"

                    # 選んだ3音を小さい順にソート
                    # 音量(振幅)は積を使うだけなのでそのまま
                    sorted_freq = [float(eval(partial1_freq)), float(eval(partial2_freq)), float(eval(partial3_freq))]
                    sorted_freq.sort()

                    m_par += modality_partial(sorted_freq[0], sorted_freq[1], sorted_freq[2], float(eval(partial1_amp)), float(eval(partial2_amp)), float(eval(partial3_amp)))
    return m_par

# 4 tones Modality
def mod_tet(root, second, third, forth, overtone_range):
    return (mod_tri(root, second, third, overtone_range) + mod_tri(root, second, forth, overtone_range) + mod_tri(root, third, forth, overtone_range) + mod_tri(second, third, forth, overtone_range)) / 4

# 3 tones Instability
def ins_tri(root, second, third, overtone_range):
    return dis_tri(root, second, third, overtone_range) + sigma * ten_tri(root, second, third, overtone_range)

# 4 tones Instability
def ins_tet(root, second, third, forth, overtone_range):
    return dis_tet(root, second, third, forth, overtone_range) + sigma * ten_tet(root, second, third, forth, overtone_range)

if __name__ == "__main__":
    main()