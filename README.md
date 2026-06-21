# Online Retail Data Pipeline

Small batch data pipeline built with Python and PostgreSQL.

The project uses the UCI Online Retail dataset and follows a simple warehouse-style flow:

```text
Excel file --> raw table --> staging table --> fact/dimension tables --> sales marts
```

The goal is to practice the core parts of a data engineering workflow: loading data, cleaning it, modeling it, building aggregates, and checking that the numbers still match after transformations.

## Dataset

Source: UCI Online Retail dataset

The raw file contains 541,909 rows and 8 columns:

- `InvoiceNo`
- `StockCode`
- `Description`
- `Quantity`
- `InvoiceDate`
- `UnitPrice`
- `CustomerID`
- `Country`

The dataset includes normal sales, cancelled invoices, missing customer IDs, missing descriptions, and some technical/adjustment rows.

## Stack

- Python
- pandas
- psycopg
- PostgreSQL
- Git

## Pipeline

The pipeline is split into three scripts:

```text
scripts/load_raw.py       loads the Excel file into PostgreSQL
scripts/build_models.py   builds staging, fact, dimension, and mart tables
scripts/run_pipeline.py   runs the full pipeline
```

There is also a small connection check script:

```text
scripts/check_db_connection.py
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

### stg_online_retail

Cleans and prepares the data for modeling.

Main logic:

- trims empty descriptions
- casts `customer_id` to integer
- marks cancelled invoices with `invoice_no LIKE 'C%'`
- marks valid sales as non-cancelled rows with positive quantity and positive unit price
- calculates `revenue = quantity * unit_price`

### fact_invoice_items

Contains only valid sales rows.

### dim_products

One row per product stock code.

### dim_customers

One row per known customer. Rows with missing `customer_id` stay in the fact table but are not added to the customer dimension.

### mart_daily_sales

Daily sales summary.

### mart_country_sales

Country-level sales summary.

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

The project keeps invalid or technical rows in staging, but excludes them from the sales fact table.

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
Revenue validation passed!
Built stg_online_retail.
Built fact_invoice_items.
Built dim_products.
Built dim_customers.
Built mart_daily_sales.
Built mart_country_sales.
Pipeline finished successfully!
```

## Current Limitations

This is a first version of the project. Some things are intentionally still simple:

- SQL transformations are currently inside the Python script
- database connection settings are hardcoded for local development
- there is no scheduler yet
- there is no dashboard yet
- there are no automated tests yet

## Planned Improvements

- move SQL transformations into separate `.sql` files
- add a separate data quality report
- add dbt models
- add scheduling with cron or Airflow
- add a small dashboard
- add Docker for easier local setup