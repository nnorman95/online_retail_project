# Online Retail Data Pipeline

Small batch data pipeline built with Python, PostgreSQL, and SQL files.

The project uses the UCI Online Retail dataset and follows a simple warehouse-style flow:

```text
Excel file --> raw table --> staging table --> fact/dimension tables --> sales marts --> validation
```

The goal is to practice the core parts of a data engineering workflow: loading data, checking data quality, cleaning and modeling data, building analytical tables, and validating that important metrics still match after transformations.

## Dataset

Source: UCI Online Retail dataset

The raw file contains 541,909 rows and 8 columns:

* `InvoiceNo`
* `StockCode`
* `Description`
* `Quantity`
* `InvoiceDate`
* `UnitPrice`
* `CustomerID`
* `Country`

The dataset includes normal sales, cancelled invoices, missing customer IDs, missing descriptions, and some technical or adjustment rows.

## Stack

* Python
* pandas
* psycopg
* PostgreSQL
* SQL
* Git

## Project Structure

```text
.
├── README.md
├── requirements.txt
├── data/
│   └── raw/
│       └── online_retail.xlsx
├── scripts/
│   ├── load_raw.py
│   ├── build_models.py
│   ├── run_pipeline.py
│   ├── data_quality_report.py
│   └── check_db_connection.py
└── sql/
    ├── 01_create_staging.sql
    ├── 02_create_fact_invoice_items.sql
    ├── 03_create_dim_products.sql
    ├── 04_create_dim_customers.sql
    ├── 05_create_mart_daily_sales.sql
    ├── 06_create_mart_country_sales.sql
    ├── 07_validate_revenue.sql
    └── 08_data_quality_report.sql
```

The Excel dataset is not intended to be committed to Git. It should be placed locally in:

```text
data/raw/online_retail.xlsx
```

## Pipeline

The pipeline is split into Python scripts and SQL model files.

Python scripts:

```text
scripts/load_raw.py              loads the Excel file into PostgreSQL
scripts/build_models.py          runs SQL files and builds the data model
scripts/run_pipeline.py          runs the full pipeline
scripts/data_quality_report.py   prints a data quality summary
```

There is also a small connection check script:

```text
scripts/check_db_connection.py
```

SQL files:

```text
sql/01_create_staging.sql              creates the staging table
sql/02_create_fact_invoice_items.sql   creates the sales fact table
sql/03_create_dim_products.sql         creates the product dimension
sql/04_create_dim_customers.sql        creates the customer dimension
sql/05_create_mart_daily_sales.sql     creates the daily sales mart
sql/06_create_mart_country_sales.sql   creates the country sales mart
sql/07_validate_revenue.sql            checks revenue consistency
sql/08_data_quality_report.sql         returns data quality metrics
```

## Data Model

The pipeline creates these PostgreSQL tables:

```text
raw_online_retail
stg_online_retail
fact_invoice_items
dim_products
dim_customers
mart_daily_sales
mart_country_sales
```

### raw_online_retail

Raw copy of the source data, with column names converted to snake_case.

This layer keeps the source data close to its original form.

### stg_online_retail

Cleans and prepares the data for modeling.

Main logic:

* trims empty descriptions
* casts `customer_id` to integer
* marks cancelled invoices with `invoice_no LIKE 'C%'`
* marks valid sales as non-cancelled rows with positive quantity and positive unit price
* calculates `revenue = quantity * unit_price`

### fact_invoice_items

Contains only valid sales rows.

Cancelled invoices, zero-price rows, negative-price rows, and other invalid rows are excluded from this fact table.

### dim_products

One row per product stock code.

For this version, product names are selected with a simple `MAX(description)` rule.

### dim_customers

One row per known customer.

Rows with missing `customer_id` stay in the fact table and sales marts, but are not added to the customer dimension.

### mart_daily_sales

Daily sales summary with:

* total orders
* total items
* total quantity
* total revenue

### mart_country_sales

Country-level sales summary with:

* total orders
* total items
* total quantity
* total revenue

## Data Quality Notes

Initial checks found:

```text
total rows: 541,909
null descriptions: 1,454
null customer IDs: 135,080
quantity <= 0: 10,624
unit_price <= 0: 2,517
cancelled invoice rows: 9,288
valid sale rows: 530,104
```

Cancelled invoices are identified by invoice numbers starting with `C`.

The project keeps invalid or technical rows in staging, but excludes them from the final sales fact table.

A separate data quality report can be generated with:

```bash
python scripts/data_quality_report.py
```

Example output:

```text
Data Quality Report
-------------------
total_rows: 541909
null_descriptions: 1454
null_customer_ids: 135080
non_positive_quantity_rows: 10624
non_positive_unit_price_rows: 2517
cancelled_rows: 9288
valid_sale_rows: 530104
invalid_sale_rows: 11805
first_invoice_at: 2010-12-01 08:26:00
last_invoice_at: 2011-12-09 12:50:00
country_count: 38
valid_revenue: 10666684.54
```

## Revenue Validation

After building the final tables, the pipeline checks that revenue matches across:

```text
fact_invoice_items
mart_daily_sales
mart_country_sales
```

Expected validated revenue:

```text
10,666,684.54
```

This check is included to catch accidental row loss or duplicated revenue during transformations.

## How to Run

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the full pipeline:

```bash
python scripts/run_pipeline.py
```

Expected output:

```text
Running scripts/load_raw.py...
Rows loaded: 541909
Running scripts/build_models.py...
Built from 01_create_staging.sql
Built from 02_create_fact_invoice_items.sql
Built from 03_create_dim_products.sql
Built from 04_create_dim_customers.sql
Built from 05_create_mart_daily_sales.sql
Built from 06_create_mart_country_sales.sql
Revenue validation passed!
Pipeline finished successfully!
```

Run the data quality report:

```bash
python scripts/data_quality_report.py
```

## Current Limitations

This is a local first version of the project. Some parts are intentionally still simple:

* database connection settings are hardcoded for local development
* the raw Excel file must be downloaded and placed manually
* there is no scheduler yet
* there is no dashboard yet
* there are no automated tests yet
* product naming logic is simple and can be improved
* SQL files are executed by a Python script instead of a dedicated transformation tool like dbt
