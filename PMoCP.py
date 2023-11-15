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

pitchName = ["C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
             "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
             "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", 
             "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5", 
             "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6"]

F0_freqDict = dict(zip(pitchName, F0_freq))
F1_freqDict = dict(zip(pitchName, F1_freq))
F2_freqDict = dict(zip(pitchName, F2_freq))
F3_freqDict = dict(zip(pitchName, F3_freq))
F4_freqDict = dict(zip(pitchName, F4_freq))
F5_freqDict = dict(zip(pitchName, F5_freq))

F0_ampDict = dict(zip(pitchName, F0_amp))
F1_ampDict = dict(zip(pitchName, F1_amp))
F2_ampDict = dict(zip(pitchName, F2_amp))
F3_ampDict = dict(zip(pitchName, F3_amp))
F4_ampDict = dict(zip(pitchName, F4_amp))
F5_ampDict = dict(zip(pitchName, F5_amp))

# -----------------------------------------------------------------------------

def main():
    overtone_range = 6
    
    print("You can use these notes.")
    print(pitchName)
    
    # 和音構成音数の入力
    print("number of notes(2~4) : ", end="")
    n = input()

    # 数値でなければ終了
    if not(n.isdecimal()):
        print("Number of notes is inappropriate.")
        return
    
    num = int(n)

    # 2音のとき，不協和度のみ算出
    if num == 2:
        print("first : ", end="") 
        firstD = input()
        print("second : ", end="") 
        secondD = input()

        if (firstD in pitchName) and (secondD in pitchName):
            print("This cord is composed of " + firstD + ", " + secondD + ". \n")

            print("Dissonnace : " + str(dis_bi(firstD, secondD, overtone_range)))
            print("Tension, Modality and Instability cannot be defined.")
        # 入力された音名が正しくないとき処理をしない
        else:
            print("Note is inappropriate.")

    # 3音のとき，4項目算出
    elif num == 3:
        print("first : ", end="") 
        firstD = input()
        print("second : ", end="") 
        secondD = input()
        print("third : ", end="")
        thirdD = input()

        if (firstD in pitchName) and (secondD in pitchName) and (thirdD in pitchName):
            print("This cord is composed of " + firstD + ", " + secondD + ", " + thirdD + ". \n")

            print("Dissonnace : " + str(dis_tri(firstD, secondD, thirdD, overtone_range)))
            print("Tension : " + str(ten_tri(firstD, secondD, thirdD, overtone_range)))
            print("Modality : " + str(mod_tri(firstD, secondD, thirdD, overtone_range)))
            print("Instability : " + str(ins_tri(firstD, secondD, thirdD, overtone_range)))
        # 入力された音名が正しくないとき処理をしない
        else:
            print("Note is inappropriate.")

    # 4音のとき，4項目算出
    elif num == 4:
        print("first : ", end="") 
        firstD = input()
        print("second : ", end="") 
        secondD = input()
        print("third : ", end="")
        thirdD = input()
        print("forth : ", end="")  
        forthD = input()
        if (firstD in pitchName) and (secondD in pitchName) and (thirdD in pitchName) and (forthD in pitchName):
            print("This cord is composed of " + firstD + ", " + secondD + ", " + thirdD + ", " + forthD + ". \n")

            print("Dissonnace : " + str(dis_tet(firstD, secondD, thirdD, forthD, overtone_range)))
            print("Tension : " + str(ten_tet(firstD, secondD, thirdD, forthD, overtone_range)))
            print("Modality : " + str(mod_tet(firstD, secondD, thirdD, forthD, overtone_range)))
            print("Instability : " + str(ins_tet(firstD, secondD, thirdD, forthD, overtone_range)))
        # 入力された音名が正しくないとき処理をしない
        else:
            print("Note is inappropriate.")

    # 構成音数が2,3,4以外のとき，処理をしない
    else:
        print("Number of notes is inappropriate.")

    return


# C2, Cs2, ..., A6
#  0,   1, ..., 57

# Dissonance caliculation
def dissonance_partial(f1, f2, a1, a2):
    return  a1 * a2 * beta3 * (math.exp((-1) * beta1 * math.log(f2 / f1, b) ** gamma) - math.exp((-1) * beta2 * math.log(f2 / f1, b) ** gamma))

# 2 tones Dissonance
def dis_bi(root, second, overtone_range):

    for o_r in range(0,overtone_range):
        d_par = 0
        for i in range(0, o_r+1):
            for j in range(0, o_r+1):
                partial1_amp = "F" + str(i) + "_ampDict[\"" + root + "\"]"
                partial2_amp = "F" + str(j) + "_ampDict[\"" + second + "\"]"
                partial1_freq = "F" + str(i) + "_freqDict[\"" + root + "\"]"
                partial2_freq = "F" + str(j) + "_freqDict[\"" + second + "\"]"

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
                    partial1_amp = "F" + str(i) + "_ampDict[\"" + root + "\"]"
                    partial2_amp = "F" + str(j) + "_ampDict[\"" + second + "\"]"
                    partial3_amp = "F" + str(k) + "_ampDict[\"" + third + "\"]"
                    partial1_freq = "F" + str(i) + "_freqDict[\"" + root + "\"]"
                    partial2_freq = "F" + str(j) + "_freqDict[\"" + second + "\"]"
                    partial3_freq = "F" + str(k) + "_freqDict[\"" + third + "\"]"

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
                    partial1_amp = "F" + str(i) + "_ampDict[\"" + root + "\"]"
                    partial2_amp = "F" + str(j) + "_ampDict[\"" + second + "\"]"
                    partial3_amp = "F" + str(k) + "_ampDict[\"" + third + "\"]"
                    partial1_freq = "F" + str(i) + "_freqDict[\"" + root + "\"]"
                    partial2_freq = "F" + str(j) + "_freqDict[\"" + second + "\"]"
                    partial3_freq = "F" + str(k) + "_freqDict[\"" + third + "\"]"

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