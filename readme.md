# 3D Android Face Expression Generation

## 必要なモジュールのインストール手順
1. `conda`を使用して仮想環境`face3D`を作成します。
```sh
conda create --name face3D python=3.9
```
2. 仮想環境をアクティベートします。
```sh
conda activate face3D
```
3. `requirements.txt`ファイルを使用して必要なモジュールをインストールします。
```sh
pip install -r requirements.txt
```
## `ex.py`プログラムの説明

`ex.py`は、3Dモデルの特定のポイントを基準にしてモデルを正規化するプログラムです。以下の手順で動作します。

1. モデルポイントと基準ポイントをnumpy配列に変換します。
2. モデルポイントと基準ポイントの重心を計算します。
3. モデルポイントと基準ポイントを重心に合わせて平行移動します。
4. SVDを使用して回転行列を計算します。
5. 回転行列をメッシュの頂点に適用します。
6. 正規化されたメッシュを作成し、保存します。

## 実行方法

1. 仮想環境`face3D`をアクティベートします。

```sh
conda activate face3D
```

2. `ex.py`を実行します。

```sh
python ex.py
```

これで、プログラムが実行され、正規化された3Dモデルが保存されます。
