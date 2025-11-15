# AI エージェントアプリテンプレート（Bolt for Python）

この Bolt for Python テンプレートは、Slack で [AI Apps](https://docs.slack.dev/ai/) を構築する方法を紹介します。

[OpenAI](https://openai.com) のモデルを利用しており、あらゆる種類のプロンプトに合わせてカスタマイズできます。

## セットアップ

作業を始める前に、アプリをインストールする権限を持つ開発用ワークスペースがあることを確認してください。まだ用意していない場合は [こちら](https://slack.com/create) から作成できます。

### デベロッパープログラム

アプリの構築とテスト向けに用意されたサンドボックス環境、ツール、リソースへアクセスできる [Slack Developer Program](https://api.slack.com/developer-program) に参加してください。

## インストール

Slack CLI もしくはその他の開発ツールを使ってこのアプリを自分のワークスペースに追加し、その後 **[Providers](#providers)** セクションを読み進めて LLM の応答設定を行います。

### Slack CLI を使う場合

ご利用の OS 向けに Slack CLI の最新バージョンをインストールします。

- [Slack CLI（macOS / Linux）](https://docs.slack.dev/tools/slack-cli/guides/installing-the-slack-cli-for-mac-and-linux/)
- [Slack CLI（Windows）](https://docs.slack.dev/tools/slack-cli/guides/installing-the-slack-cli-for-windows/)

Slack CLI を初めて使う場合はログインも必要です。

```sh
slack login
```

#### プロジェクトの初期化

```sh
slack create my-bolt-python-assistant --template slack-samples/bolt-python-assistant-template
cd my-bolt-python-assistant
```

#### Slack アプリの作成

次のコマンドで新しい Slack アプリを開発用ワークスペースに追加します。今後の開発に備えて「local」アプリ環境を選択してください。

```sh
slack install
```

Slack アプリが作成できたら、次は LLM プロバイダーの設定に進みましょう。

### 端末を使う場合

1. [https://api.slack.com/apps/new](https://api.slack.com/apps/new) を開き、「From an app manifest」を選択します。
2. アプリをインストールしたいワークスペースを選びます。
3. [manifest.json](./manifest.json) の内容を JSON タブ内の `*Paste your manifest code here*` と表示されたテキストボックスに貼り付け、_Next_ をクリックします。
4. 設定を確認し、_Create_ をクリックします。
5. _Install to Workspace_ をクリックし、続く画面で _Allow_ を押します。するとアプリ設定ダッシュボードにリダイレクトされます。

#### 環境変数

アプリを実行する前に、以下の環境変数を保存します。

1. `.env.sample` を `.env` にリネームします。
2. [このリスト](https://api.slack.com/apps) からアプリの設定ページを開き、左側メニューの _OAuth & Permissions_ をクリックし、_Bot User OAuth Token_ を `.env` ファイルの `SLACK_BOT_TOKEN` にコピーします。

```sh
SLACK_BOT_TOKEN=YOUR_SLACK_BOT_TOKEN
```

3. 左側メニューの _Basic Information_ を開き、_App-Level Tokens_ セクションの手順に従って `connections:write` スコープを持つアプリレベルトークンを作成します。そのトークンを `.env` の `SLACK_APP_TOKEN` にコピーします。

```sh
SLACK_APP_TOKEN=YOUR_SLACK_APP_TOKEN
```

#### プロジェクトの初期化

```sh
git clone https://github.com/slack-samples/bolt-python-assistant-template.git my-bolt-python-assistant
cd my-bolt-python-assistant
```

#### Python 仮想環境のセットアップ

```sh
python3 -m venv .venv
source .venv/bin/activate  # Windows の場合は .\.venv\Scripts\Activate を使用
```

#### 依存関係のインストール

```sh
pip install -r requirements.txt
```

## プロバイダー

### OpenAI の設定

[create a new secret key](https://platform.openai.com/api-keys) をクリックして OpenAI のアカウントダッシュボードからモデルの利用を有効化し、取得した OpenAI キーを `.env` ファイルに `OPENAI_API_KEY` として保存します。

```zsh
OPENAI_API_KEY=YOUR_OPEN_API_KEY
```

## 開発

### アプリの起動

#### Slack CLI

```sh
slack run
```

#### 端末

```sh
python3 app.py
```

ボットとの会話を始めましょう！新しい DM もしくはスレッドを開始し、ボットが応答したらフィードバックボタンを押してください。

### Lint

```sh
# リンティングにはリポジトリのルートで ruff check を実行
ruff check

# コード整形には ruff format を実行
ruff format
```

## プロジェクト構成

### `manifest.json`

`manifest.json` は Slack アプリ用の設定ファイルです。マニフェストを使うことで、あらかじめ定義された設定でアプリを作成したり、既存アプリの設定を調整したりできます。

### `app.py`

`app.py` はアプリケーションのエントリーポイントで、サーバーを起動するときに実行するファイルです。このプロジェクトではこのファイルをできるだけシンプルに保ち、主に受信リクエストをルーティングする目的で使用します。

### `/listeners`

すべての受信リクエストは「リスナー」にルーティングされます。このディレクトリでは Slack プラットフォームの機能ごとにリスナーを分類しており、`/listeners/events` は受信イベント、`/listeners/shortcuts` は [Shortcuts](https://docs.slack.dev/interactivity/implementing-shortcuts/) リクエストを処理する、といった具合になっています。

**`/listeners/assistant`**

新しい Slack Assistant 機能を構成し、ユーザーが AI チャットボットとやり取りするための専用サイドパネル UI を提供します。このモジュールには次のファイルが含まれます。

- `assistant_thread_started.py`: 新しいアプリスレッドに推奨プロンプトのリストで応答します。
- `message.py`: アプリスレッドや **Chat** / **History** タブから送信されたユーザーメッセージに対して、LLM が生成した応答を返します。

### `/ai`

`llm_caller.py` は OpenAI API への接続とメッセージ整形を担当します。会話スレッドを OpenAI モデルに送信する `call_llm()` 関数が含まれています。

## アプリ配布 / OAuth

複数のワークスペースにアプリを配布する予定がある場合のみ OAuth を実装してください。関連する OAuth 設定をまとめた `app_oauth.py` も別途用意されています。

OAuth を使う場合、Slack からのリクエストを受け取れる公開 URL が必要です。このテンプレートアプリでは [`ngrok`](https://ngrok.com/download) を使用しています。セットアップ方法は [こちらのガイド](https://ngrok.com/docs#getting-started-expose) を参照してください。

`ngrok` を起動して外部ネットワークからアプリにアクセスし、OAuth 用のリダイレクト URL を作成します。

```
ngrok http 3000
```

出力には `http` と `https` のフォワーディングアドレスが含まれます（ここでは `https` を使用）。次のような形式になります。

```
Forwarding   https://3cb89939.ngrok.io -> http://localhost:3000
```

アプリ設定の **OAuth & Permissions** に移動し、**Add a Redirect URL** をクリックします。リダイレクト URL には `ngrok` のフォワーディングアドレスに `slack/oauth_redirect` パスを付与したものを指定します。例：

```
https://3cb89939.ngrok.io/slack/oauth_redirect
```
