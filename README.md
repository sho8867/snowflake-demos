# Snowflake デモ集

Snowflake 各種機能のデモ環境リポジトリです。
ブラウザ（Snowsight）だけで繰り返し構築・破棄できます。

## デモ一覧

| # | デモ | テーマ | 主な機能 |
|---|------|--------|---------|
| [01](demos/01_streamlit_dashboard/) | 売上分析ダッシュボード | 小売業 | Streamlit in Snowflake |

> デモは随時追加予定

---

## 初回セットアップ（一度だけ）

Snowsight のワークシートで以下を実行してください。
`sho8867` はご自身の GitHub ユーザー名に置き換えてください。

```sql
USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS SNOWFLAKE_QUICKSTART_REPOS
  COMMENT = 'Git Integration DB - do not drop';
CREATE SCHEMA IF NOT EXISTS SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS;

CREATE OR REPLACE API INTEGRATION demo_git_api
  API_PROVIDER         = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/sho8867/')
  ENABLED              = TRUE;

CREATE OR REPLACE GIT REPOSITORY SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO
  API_INTEGRATION = demo_git_api
  ORIGIN          = 'https://github.com/sho8867/snowflake-demos.git';

ALTER GIT REPOSITORY SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO FETCH;
```

> Intelligence デモ（別リポジトリ）で `demo_git_api` を作成済みの場合、
> API Integration の作成はスキップできます。

---

## 各デモの実行方法

各デモディレクトリの README を参照してください。
基本的な流れは共通です:

```sql
-- 最新コードを取得
ALTER GIT REPOSITORY SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO FETCH;

-- デモを構築（各デモの 00_deploy_all.sql を指定）
EXECUTE IMMEDIATE FROM
  @SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO/branches/main/demos/<demo>/assets/sql/00_deploy_all.sql;
```

---

## リポジトリ構成

```
snowflake-demos/
├── setup/
│   └── 00_git_integration.sql    # 初回のみ実行
├── demos/
│   └── 01_streamlit_dashboard/   # Streamlit 売上分析ダッシュボード
│       ├── README.md
│       ├── assets/
│       │   ├── sql/              # 00_deploy_all〜03, 99_teardown
│       │   ├── data/             # サンプル CSV
│       │   └── app/              # streamlit_app.py
│       └── docs/
└── docs/
    └── demo_catalog.md           # デモカタログ
```
