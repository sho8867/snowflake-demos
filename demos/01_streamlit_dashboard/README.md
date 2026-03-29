# Demo 01: 売上分析ダッシュボード

Streamlit in Snowflake で構築した小売業向けインタラクティブダッシュボードです。

## 画面構成

| セクション | 内容 |
|-----------|------|
| KPI カード | 総売上・販売数量・粗利益・粗利率・取引件数 |
| 月次売上推移 | 売上と粗利益の折れ線グラフ |
| カテゴリ別売上 | 横棒グラフ（粗利率をカラースケールで表示） |
| 地域別売上 | 地域ごとの売上・数量・粗利率テーブル |
| 商品別トップ10 | 売上上位10商品テーブル |
| キャンペーン実績 | チャネル別 CTR/CVR/CPA の棒グラフ + テーブル |

サイドバーで **年度・カテゴリ・地域** を絞り込むと全セクションが連動して更新されます。

---

## デプロイ手順

### 前提条件

- 初回セットアップ済み（[ルート README](../../README.md) 参照）
- ACCOUNTADMIN ロールでのログイン

### 構築

```sql
ALTER GIT REPOSITORY SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO FETCH;

EXECUTE IMMEDIATE FROM
  @SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO/branches/main/demos/01_streamlit_dashboard/assets/sql/00_deploy_all.sql;
```

### アプリを開く

Snowsight 左メニュー > **Projects > Streamlit** > `SALES_DASHBOARD`

---

## クリーンアップ

```sql
EXECUTE IMMEDIATE FROM
  @SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO/branches/main/demos/01_streamlit_dashboard/assets/sql/99_teardown.sql;
```

---

## Snowflake オブジェクト

| オブジェクト | 名前 |
|-------------|------|
| データベース | `DEMO_STREAMLIT_DB` |
| スキーマ | `DEMO_STREAMLIT_DB.ANALYTICS` |
| ウェアハウス | `DEMO_STREAMLIT_WH` |
| Streamlit | `DEMO_STREAMLIT_DB.ANALYTICS.SALES_DASHBOARD` |
| アプリステージ | `DEMO_STREAMLIT_DB.ANALYTICS.APP_STAGE` |
