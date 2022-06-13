# flask_template

Flaskの環境をDockerでワンライナーで構築、開発環境を切り離せるアプリケーションです。

## デフォルトのイメージ名

アプリケーションイメージ： app
データベースイメージ： DB


## DockerImage

* mysql:8.0-oracle
* Python:3

Flaskなどについてはpipに依存するため不定

各自必要なパッケージなどはディレクトリ直下の`docekrfile`に追記してください。

## 環境構築

テンプレートリポジトリに設定してあるので各自githubの`Use this template`からリポジトリを作成してください


### Windows(WSL2が使用できる環境が推奨です。)

* [Dockerのインストール(DockerHub)](https://docs.docker.com/desktop/windows/install/)

* [WSL2の導入(Microsoft Docs)](https://docs.microsoft.com/ja-jp/windows/wsl/install)


### Mac OS

```bash
brew install docker
brew install docker-compose
```


## 実行方法

```bash
docker-compose up --build
```
をターミナルで実行することでwebサーバーとDBサーバーが自動的に立ち上がります。

[localhost:5001](localhost:5001)が接続先URLです。（環境によって適度にポートなどを変更してください。)

## 実行フォルダの指定について

`.env`ファイル内の`FLASK_APP`環境変数で指定してください。

## ディレクトリについて

```
flask-docker
┣ database/ 
┃   └ dockerfile 
┃         - dbの設定に使うdockerfile
┣ exemple/      
┃   └ app.py     
┃         - デフォルトで読み込まれるpythonファイル
┣　initdb.d/     
┃   ┃     - db作成時に読み込まれるディレクトリ
┃   └ init.sql   
┃         - 自動でsqlが実行されるファイル
┣　.env   
┃         - docker生成の際に設定される環境変数
┣　.gitignore
┣ docker-compse.yml 
┃         - docker-composeの設定ファイル
┣ dockerfile 
┃         - appの設定ファイル
┣ LICENSE
┗ readme.md
```

## DBについて

DB(イメージ名)のcliにて
```bash
mysql -u admin -p
#パスワード
pass
```
でcliを使用することができます。

ビルド時に自動で`./initdb.d/init.sql`が読み込まれ自動でテーブルが生成されます。

テーブルを使用したい場合は適度に変更してください。

## .envについて
デフォルトでは設定のため`gitignore`に追加していませんgitのパブリックリポジトリなどに上げる際は.gitignoreに追加してください


## .envにある各変数の説明

`MYSQL_USER` mysqlが自動で生成してくれるユーザー

`MYSQL_DATABASE`mysqlが自動で生成してくれるデータベース

`MYSQL_PASSWORD` mysqlが自動で生成してくれるユーザーのパスワード

`MYSQL_ROOT_PASSWORD` mysqlのrootのパスワード

`DATABASE_HOST`DBのホスト名（イメージ名に依存します)

`FLASK_APP` Flaskで使用するファイルの指定

`FLASK_ENV` flaskへの引数


## セッションについて

デフォルトではコメントアウトしていますが、そのままでも扱うことができます。`SECRET_KEY`に関してはコンテナ生成時に自動で生成しています。


## その他

このプロジェクトの全てのコードは、特に明記されていない限り、[MIT](https://opensource.org/licenses/MIT)ライセンスの元でライセンスされています。

