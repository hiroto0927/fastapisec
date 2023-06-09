# 認証アプリ

# 要件定義

他のリソースサーバが共通して利用できる認証機能を提供するアプリケーション。

## 機能要件

- ユーザ名とパスワードでログインできる (期待値)
- ユーザが新規アカウントを発行できる
- ユーザがアカウントを破棄できる
- 管理者がユーザアカウントを削除できる

## 非機能要件

## 画面要件

## テスト (総合テスト、シナリオテスト)

### ログインのテスト

- ログインの成功テスト
  - ユーザ名とパスワードのセットがDBに保存されている状態で、正しいユーザ名とパスワードが入力された場合に、ログインに成功すること

- ログインが失敗するテスト

### ユーザが新規アカウントを発行できる

- アカウント発行シナリオテスト
   - 前提: 未登録ユーザ
   0. 登録前はログインできないことを確認する
   1. 登録項目(メールアドレス、パスワード、確認用パスワード)を入力し送信することで、メールアドレスの確認用メールが届く
   2. 確認用メールから、リンクをクリックすることで、登録が完了する
   3. 実際にログインして、ログインできることを確認する


# 基本設計

## API設計

### 新規アカウント発行のAPI

- ユーザ仮登録用API
  - メールアドレスとパスワードを受け取って、DBに情報を登録する。
  - DBに正常に登録が完了したら、200番を返すよ
  - DBに正常に登録が完了したら、メール通知するよ

### テスト (結合テスト)

- APIのテストが必要
  - 登録が可能なメールアドレスとパスワードのセットをAPIに投げて、DBに情報が登録されていることを確認する。また、200番が帰ってくることを確認する。メール送信用のメソッドが呼び出されることを確認する。


# 詳細設計

## crudsメソッド群

### メールアドレスとパスワードをDBに登録する処理 (一つの関数)

- パスワードがハッシュかされる
- メールアドレスが「****@***.com」に従う

引数: メールアドレス、パスワード
戻り値: true or false (登録した内容を返す)

### メールアドレスが既に登録済みかを確認する処理

### メール送信の処理

### テスト (単体テスト)

一つの関数に対して引数を与えて、期待の戻り値が帰ってくるかをテストする。

- aaa@bbb.com, aaaaaaaaaの組み合わせはtrue、dbには、aaa@bbb.com, a420DjbA2DDAWSICKEIが登録される
