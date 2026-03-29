-- =====================================================
-- Demo 01: Teardown - remove all demo objects
-- SNOWFLAKE_QUICKSTART_REPOS is preserved.
-- =====================================================

USE ROLE ACCOUNTADMIN;

DROP DATABASE  IF EXISTS DEMO_STREAMLIT_DB;
DROP WAREHOUSE IF EXISTS DEMO_STREAMLIT_WH;
DROP ROLE      IF EXISTS DEMO_STREAMLIT_USER;
DROP ROLE      IF EXISTS DEMO_STREAMLIT_ADMIN;

SELECT 'Demo 01 teardown complete. Git integration (SNOWFLAKE_QUICKSTART_REPOS) is preserved.' AS status;
