-- =====================================================
-- Demo 01: Create tables and load data
-- =====================================================

USE ROLE      DEMO_STREAMLIT_ADMIN;
USE WAREHOUSE DEMO_STREAMLIT_WH;
USE DATABASE  DEMO_STREAMLIT_DB;
USE SCHEMA    ANALYTICS;

-- Tables
CREATE OR REPLACE TABLE PRODUCTS (
    product_id   VARCHAR(20)   NOT NULL,
    product_name VARCHAR(100)  NOT NULL,
    category     VARCHAR(50)   NOT NULL,
    subcategory  VARCHAR(50),
    unit_price   NUMBER(10, 2) NOT NULL,
    cost_price   NUMBER(10, 2) NOT NULL,
    PRIMARY KEY (product_id)
);

CREATE OR REPLACE TABLE SALES (
    sale_id      VARCHAR(20)   NOT NULL,
    sale_date    DATE          NOT NULL,
    product_id   VARCHAR(20)   NOT NULL,
    product_name VARCHAR(100),
    category     VARCHAR(50),
    subcategory  VARCHAR(50),
    region       VARCHAR(50),
    store_id     VARCHAR(20),
    units_sold   NUMBER(10)    NOT NULL,
    revenue      NUMBER(12, 2) NOT NULL,
    cost         NUMBER(12, 2),
    PRIMARY KEY (sale_id)
);

CREATE OR REPLACE TABLE CAMPAIGNS (
    campaign_id   VARCHAR(20)   NOT NULL,
    campaign_name VARCHAR(100)  NOT NULL,
    category      VARCHAR(50),
    channel       VARCHAR(50),
    start_date    DATE,
    end_date      DATE,
    budget        NUMBER(12, 2),
    actual_spend  NUMBER(12, 2),
    impressions   NUMBER(12),
    clicks        NUMBER(10),
    conversions   NUMBER(10),
    PRIMARY KEY (campaign_id)
);

-- Internal stage for CSV files
CREATE STAGE IF NOT EXISTS DEMO_STREAMLIT_DB.ANALYTICS.RAW_DATA;

-- Copy CSV files from Git repo to internal stage
COPY FILES
    INTO @DEMO_STREAMLIT_DB.ANALYTICS.RAW_DATA
    FROM @SNOWFLAKE_QUICKSTART_REPOS.GIT_REPOS.DEMOS_REPO/branches/main/demos/01_streamlit_dashboard/assets/data/
    PATTERN = '.*\.csv';

-- File format
CREATE OR REPLACE FILE FORMAT DEMO_STREAMLIT_DB.ANALYTICS.CSV_FORMAT
    TYPE                         = 'CSV'
    SKIP_HEADER                  = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF                      = ('NULL', 'null', '')
    ENCODING                     = 'UTF-8';

-- Load tables
COPY INTO PRODUCTS
    FROM @DEMO_STREAMLIT_DB.ANALYTICS.RAW_DATA/products.csv
    FILE_FORMAT = (FORMAT_NAME = 'DEMO_STREAMLIT_DB.ANALYTICS.CSV_FORMAT');

COPY INTO SALES
    FROM @DEMO_STREAMLIT_DB.ANALYTICS.RAW_DATA/sales.csv
    FILE_FORMAT = (FORMAT_NAME = 'DEMO_STREAMLIT_DB.ANALYTICS.CSV_FORMAT');

COPY INTO CAMPAIGNS
    FROM @DEMO_STREAMLIT_DB.ANALYTICS.RAW_DATA/campaigns.csv
    FILE_FORMAT = (FORMAT_NAME = 'DEMO_STREAMLIT_DB.ANALYTICS.CSV_FORMAT');

-- Verify
SELECT 'PRODUCTS'  AS table_name, COUNT(*) AS row_count FROM PRODUCTS  UNION ALL
SELECT 'SALES'     AS table_name, COUNT(*) AS row_count FROM SALES      UNION ALL
SELECT 'CAMPAIGNS' AS table_name, COUNT(*) AS row_count FROM CAMPAIGNS;

SELECT '02_load_data: done' AS status;
