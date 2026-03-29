-- =====================================================
-- Demo 01: Deploy Streamlit app
-- Copy app files from Git repo to stage, then create Streamlit object
-- =====================================================

USE ROLE      DEMO_STREAMLIT_ADMIN;
USE WAREHOUSE DEMO_STREAMLIT_WH;
USE DATABASE  DEMO_STREAMLIT_DB;
USE SCHEMA    ANALYTICS;

-- Stage for Streamlit app files
CREATE STAGE IF NOT EXISTS DEMO_STREAMLIT_DB.ANALYTICS.APP_STAGE
    DIRECTORY = (ENABLE = TRUE);

-- Copy app files from Git repo to stage
COPY FILES
    INTO @DEMO_STREAMLIT_DB.ANALYTICS.APP_STAGE
    FROM @SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO/branches/main/demos/01_streamlit_dashboard/assets/app/
    PATTERN = '.*\.py';

ALTER STAGE DEMO_STREAMLIT_DB.ANALYTICS.APP_STAGE REFRESH;

-- Verify app file is in stage
SELECT relative_path, size, last_modified
FROM DIRECTORY(@DEMO_STREAMLIT_DB.ANALYTICS.APP_STAGE);

-- Create Streamlit app
CREATE OR REPLACE STREAMLIT DEMO_STREAMLIT_DB.ANALYTICS.SALES_DASHBOARD
    ROOT_LOCATION = '@DEMO_STREAMLIT_DB.ANALYTICS.APP_STAGE'
    MAIN_FILE     = 'streamlit_app.py'
    QUERY_WAREHOUSE = 'DEMO_STREAMLIT_WH'
    COMMENT       = 'Retail sales analytics dashboard';

-- Grant access to USER role
GRANT USAGE ON STREAMLIT DEMO_STREAMLIT_DB.ANALYTICS.SALES_DASHBOARD TO ROLE DEMO_STREAMLIT_USER;

SELECT '03_deploy_app: done' AS status;
SELECT 'Open Snowsight > Projects > Streamlit > SALES_DASHBOARD to launch.' AS next_step;
