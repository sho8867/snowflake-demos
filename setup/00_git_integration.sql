-- =====================================================
-- One-time setup: Git Integration for snowflake-demos repo
--
-- Run this once per Snowflake account.
-- Reuses SNOWFLAKE_QUICKSTART_REPOS DB and demo_git_api
-- already created for the intelligence demo (if available).
-- =====================================================

USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS SNOWFLAKE_QUICKSTART_REPOS
    COMMENT = 'Git Integration DB - do not drop';
CREATE SCHEMA IF NOT EXISTS SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS;

-- API Integration (shared with intelligence demo)
CREATE OR REPLACE API INTEGRATION demo_git_api
    API_PROVIDER         = git_https_api
    API_ALLOWED_PREFIXES = ('https://github.com/sho8867/')
    ENABLED              = TRUE;

-- Git Repository for this demos collection
CREATE OR REPLACE GIT REPOSITORY SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO
    API_INTEGRATION = demo_git_api
    ORIGIN          = 'https://github.com/sho8867/snowflake-demos.git';

ALTER GIT REPOSITORY SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO FETCH;

SELECT 'Git integration setup complete.' AS status;
