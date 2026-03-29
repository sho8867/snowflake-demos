# CLAUDE.md — snowflake_demos

Snowflake 各種機能のデモ環境集。
接続・認証情報は `../CLAUDE.md` を参照。

## プロジェクト情報

- **GitHub リポジトリ**: https://github.com/sho8867/snowflake-demos
- **ローカルパス**: `/Users/sho/claude-code/snowflake_demos`

## Snowflake オブジェクト（共通）

| オブジェクト | 名前 |
|-------------|------|
| Git Repository | `SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO` |
| API Integration | `demo_git_api`（intelligence デモと共用） |

## デモ一覧

| # | ディレクトリ | テーマ | DB |
|---|------------|--------|-----|
| 01 | `demos/01_streamlit_dashboard/` | 小売業 売上分析ダッシュボード | `DEMO_STREAMLIT_DB` |

## 新デモ追加時のルール

- ディレクトリ: `demos/<連番>_<名前>/`
- DB名: `DEMO_<名前>_DB`（teardown で安全に削除できるよう分離）
- SQL ファイルは ASCII のみ（マルチバイト文字不可）
- 全 SQL は冪等（CREATE OR REPLACE / IF NOT EXISTS）
- `99_teardown.sql` は必ず実装する

## 開発ワークフロー

### SnowSQL で動作確認
```bash
snowsql -c demo -f demos/01_streamlit_dashboard/assets/sql/<file>.sql
```

### Snowsight でデプロイ
```sql
ALTER GIT REPOSITORY SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO FETCH;
EXECUTE IMMEDIATE FROM @SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO/branches/main/demos/01_streamlit_dashboard/assets/sql/00_deploy_all.sql;
```
