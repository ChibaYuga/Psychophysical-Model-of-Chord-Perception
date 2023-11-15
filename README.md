# 和音認知に関する心理物理モデル（Psychophysical Model of Chord Perception）[1, 2]
和音認知に関する心理物理モデル（以降，和音性モデル）は不協和度（Dissonance），緊張度（Tension），モダリティ（Modality），不安定性（Instability）の四項目からなる．

- 不協和度は2つの音を同時に鳴らしたときの響きがいかに濁っているか（協和していないか）を表す指標である
- 緊張度は3つの音からなる和音が緊張的・未解決的な響きをどのくらい持つかを表す指標である
- モダリティは解決的な3つの音からなる和音が，長調的あるいは短調的な響きをどのくらい持つかを表す指標である
- 不安定度は不協和度と緊張度双方を考慮した，和音がどのくらい不安定かを表す指標である

# プログラム
### dissonance_bi.py
  - 2音からなる和音の不協和度を算出する
  - 低い方の音を固定し，2音目を半音ずつ推移させた様子をプロットする


### dissonance_tri.py, tension_tri.py, modality_tri.py, instability.py
  - 3音からなる和音の各項目を算出しプロットする
  - 低い方の2音を固定し，3音目を半音ずつ推移させた様子をプロットする


### dissonance_tet.py, tension_tet.py, modality_tet.py, instability.py
  - 4音からなる和音の各項目を算出しプロットする  
  - 低い方の3音を固定し，4音目を半音ずつ推移させた様子をプロットする


### PMoCP.py
  - 和音を構成する音を入力すると，その和音の和音性モデル各項目が出力される


# csvファイル
和音性モデル各項目を算出するために必要な音のデータ

### sampleC4C6_dB0.csv
  - 各倍音成分が全て0dBであると仮定した音圧レベルデータ（C4~C6）
### sampleC4C6_freq.csv
  - 12平均律における各倍音成分の周波数データ（C4~C6）
### pianoC2CA6_dB.csv
  - ピアノ音（ソフトウエア音源）の各倍音成分の音圧レベルデータ（C2~A6）
  - 上記C4~C6
### pianoC2A6_freq.csv
  - ピアノ音（ソフトウエア音源）の各倍音成分の周波数データ（C2~A6）


# 参考
- [1] Cook, N. D., & Fujisawa, T. X. (2006). The psychophysics of harmony perception: Harmony is a three-tone phenomenon.
- [2] 藤澤隆史, 長田典子, & 片寄晴弘. (2006). 和音認知に関する心理物理モデル. 情報処理学会研究報告音楽情報科学 (MUS), 2006 (90(2006-MUS-066)), 99–104.
