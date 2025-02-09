from flask import Flask, jsonify
import pandas as pd
import glob
import os
import chardet

app = Flask(__name__)

@app.route('/csv_to_json', methods=['GET'])  # GETリクエストを受け付ける
def csv_to_json():
    """
    ダウンロードフォルダ内のmfmedataフォルダにあるCSVファイルを全て読み込み、
    JSON形式に変換して返すAPIエンドポイント

    Returns:
        str: JSON形式の文字列
    """
    try:
        download_folder = os.path.expanduser("~/Downloads")
        folder_path = os.path.join(download_folder, "mfmedata")

        # フォルダ内のCSVファイルを全て読み込み、データフレームに結合
        all_df = pd.DataFrame()
        for filename in glob.glob(os.path.join(folder_path, "収入・支出詳細_*.csv")):
            
            # ファイルのエンコーディングを検出
            with open(filename, 'rb') as f:
                result = chardet.detect(f.read())
            encoding = result['encoding']

            # 検出したエンコーディングでCSVファイルを読み込む
            df = pd.read_csv(filename, encoding=encoding)
            
            all_df = pd.concat([all_df, df])

        # データフレームをJSON形式に変換
        json_data = all_df.to_json(orient='records')

        # JSONデータを返す
        return jsonify(json_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)