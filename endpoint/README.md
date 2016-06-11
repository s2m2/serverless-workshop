# ファイルアップローダー＋ルーティングAPI

## 前提条件
ファイルをアップロードするS3バケットを作成しておく必要があります。

## ファイルアップローダーの使い方
1.環境変数の設定  
export AWS_ACCESS_KEY_ID="アクセスキーID"  
export AWS_SECRET_ACCESS_KEY="シークレットアクセスキー"  

2.ファイルアップロード  
python uploader.py ファイルパス  

## ルーティングAPI
AWS Lambdaに以下のように登録します。

###Configuration
Runtime: Python 2.7  
Handler: lambda_function.siimii_fileupload  
Role: S3 Execution Role  
Timeout: 任意ですが短すぎると上手くいかない  

###EventSource
EventSourceType: S3  
EventType: ObjectCreated  
Prefix: upload_  
