-- =====================================================
-- Demo 01: Streamlit Sales Dashboard - Deploy All
-- =====================================================

EXECUTE IMMEDIATE FROM @SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO/branches/main/demos/01_streamlit_dashboard/assets/sql/01_setup_db.sql;
EXECUTE IMMEDIATE FROM @SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO/branches/main/demos/01_streamlit_dashboard/assets/sql/02_load_data.sql;
EXECUTE IMMEDIATE FROM @SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO/branches/main/demos/01_streamlit_dashboard/assets/sql/03_deploy_app.sql;

SELECT 'Demo 01 deployment complete. Open Snowsight > Projects > Streamlit to launch the app.' AS status;
