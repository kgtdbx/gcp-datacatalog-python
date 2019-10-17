# gcp-datacatalog-python

Self-contained ready-to-use Python scripts to help Data Citizens who work with [Google Cloud Data Catalog][1].

[![CircleCI][2]][3]

- [Quickstart](#3-quickstart): sample code for Data Catalog's API core features.

- [Load Tag Templates from CSV files](#4-load-tag-templates-from-csv-files): loads a set of fields from **CSV files**
and creates Tag Templates using them.

- [Load Tag Templates from Google Sheets](#5-load-tag-templates-from-google-sheets): loads a set of fields from
**Google Sheets** and creates Tag Templates using them.


## 1. Understand the concepts behind this code

- [Data Catalog hands-on guide: a mental model][4] @ Google Cloud Community / Medium

- [Data Catalog hands-on guide: search, get & lookup with Python][5] @ Google Cloud Community / Medium

- [Data Catalog hands-on guide: templates & tags with Python][6] @ Google Cloud Community / Medium

## 2. Environment setup

### 2.1. Get the code

````bash
git clone https://github.com/ricardolsmendes/gcp-datacatalog-python.git
cd gcp-datacatalog-python
````

### 2.2. Auth credentials

##### 2.2.1. Create a service account and grant it below roles

- BigQuery Admin
- Data Catalog Admin

##### 2.2.2. Download a JSON key and save it as
- `./credentials/datacatalog-samples.json`

### 2.3. Virtualenv

Using *virtualenv* is optional, but strongly recommended unless you use [Docker](#24-docker).

##### 2.3.1. Install Python 3.6+

##### 2.3.2. Create and activate an isolated Python environment

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

##### 2.3.3. Install the dependencies

```bash
pip install --upgrade -r requirements.txt
```

##### 2.3.4. Set environment variables

```bash
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/datacatalog-samples.json
```

### 2.4. Docker

Docker may be used as an alternative to run all the scripts. In this case please disregard the
[Virtualenv](#23-virtualenv) install instructions. 

### 2.5. End-to-end tests

Ent-to-end tests help to make sure Google Cloud APIs and Service Accounts IAM Roles have been properly set up before
running a script. They actually communicate with the APIs and create temporary resources that are deleted just after
being used.

## 3. Quickstart

### 3.1. e2e tests

- pytest

```bash
export GOOGLE_CLOUD_TEST_ORGANIZATION_ID=ORGANIZATION_ID
export GOOGLE_CLOUD_TEST_PROJECT_ID=PROJECT_ID

pytest tests_e2e/quickstart_test.py
```

- docker

```bash
docker build --rm --tag gcp-datacatalog-python .
docker run --rm --tty \
  --env GOOGLE_CLOUD_TEST_ORGANIZATION_ID=ORGANIZATION_ID \
  --env GOOGLE_CLOUD_TEST_PROJECT_ID=PROJECT_ID \
  gcp-datacatalog-python \
  pytest tests_e2e/quickstart_test.py
```

### 3.2. quickstart.py

- python

```bash
python quickstart.py --organization-id ORGANIZATION_ID --project-id PROJECT_ID
```

- docker

```bash
docker build --rm --tag gcp-datacatalog-python .
docker run --rm --tty gcp-datacatalog-python \
  python quickstart.py --organization-id ORGANIZATION_ID --project-id PROJECT_ID
```

## 4. Load Tag Templates from CSV files

### 4.1. Provide CSV files representing the Template to be created

1. A **master file** named with the Template ID — i.e., `template-abc.csv` if your Template ID is *template_abc*.
This file may contain as many lines as needed to represent the template. The first line is always discarded as it's
supposed to contain headers. Each field line must have 3 values: the first is the Field ID; second is its Display Name;
third is the Type. Currently, types `BOOL`, `DOUBLE`, `ENUM`, `STRING`, `TIMESTAMP`, and `MULTI` are supported. *`MULTI`
is not a Data Catalog native type, but a flag that instructs the script to create a specific template to represent
field's predefined values (more on this below...)*.  
1. If the template has **ENUM fields**, the script looks for a "display names file" for each of them. The files shall
be named with the fields' names — i.e., `enum-field-xyz.csv` if an ENUM Field ID is *enum_field_xyz*. Each file must
have just one value per line, representing a display name.
1. If the template has **multivalued fields**, the script looks for a "values file" for each of them. The files shall
be named with the fields' names — i.e., `multivalued-field-xyz.csv` if a multivalued Field ID is
*multivalued_field_xyz*. Each file must have just one value per line, representing a short description for the value.
The script will generate Field's ID and Display Name based on it.
1. All Fields' IDs generated by the script will be formatted to snake case (e.g., foo_bar_baz), but it will do the
formatting job for you. So, just provide the IDs as strings.

*TIP: keep all template-related files in the same folder (`sample-input/load-template-csv` for reference).*

### 4.2. e2e tests

- pytest

```bash
export GOOGLE_CLOUD_TEST_PROJECT_ID=PROJECT_ID

pytest tests_e2e/load_template_csv_test.py
```

- docker

```bash
docker build --rm --tag gcp-datacatalog-python .
docker run --rm --tty \
  --env GOOGLE_CLOUD_TEST_PROJECT_ID=PROJECT_ID \
  gcp-datacatalog-python \
  pytest tests_e2e/load_template_csv_test.py
```

### 4.3. load_template_csv.py

- python

```bash
python load_template_csv.py \
  --template-id TEMPLATE_ID --display-name DISPLAY_NAME \
  --project-id PROJECT_ID --files-folder FILES_FOLDER \
  [--delete-existing]
```

- docker

```bash
docker build --rm --tag gcp-datacatalog-python .
docker run --rm --tty gcp-datacatalog-python \
  python load_template_csv.py \
  --template-id TEMPLATE_ID --display-name DISPLAY_NAME \
  --project-id PROJECT_ID --files-folder FILES_FOLDER \
  [--delete-existing]
```

## 5. Load Tag Templates from Google Sheets

### 5.1. Enable the Google Sheets API in your GCP Project

https://console.developers.google.com/apis/library/sheets.googleapis.com?project=<PROJECT_ID>

### 5.2. Provide Google Spreadsheets representing the Template to be created

1. A **master sheet** named with the Template ID — i.e., `template-abc` if your Template ID is *template_abc*. This
sheet may contain as many lines as needed to represent the template. The first line is always discarded as it's
supposed to contain headers. Each field line must have 3 values: column A is the Field ID; column B is its Display Name;
column C is the Type. Currently, types `BOOL`, `DOUBLE`, `ENUM`, `STRING`, `TIMESTAMP`, and `MULTI` are supported.
*`MULTI` is not a Data Catalog native type, but a flag that instructs the script to create a specific template to
represent field's predefined values (more on this below...)*.  
1. If the template has **ENUM fields**, the script looks for a "display names sheet" for each of them. The sheets shall
be named with the fields' names — i.e., `enum-field-xyz` if an ENUM Field ID is *enum_field_xyz*. Each sheet must have
just one value per line (column A), representing a display name.
1. If the template has **multivalued fields**, the script looks for a "values sheet" for each of them. The sheets shall
be named with the fields' names — i.e., `multivalued-field-xyz` if a multivalued Field ID is *multivalued_field_xyz*.
Each sheet must have just one value per line (column A), representing a short description for the value. The script
will generate Field's ID and Display Name based on it.
1. All Fields' IDs generated by the script will be formatted to snake case (e.g., foo_bar_baz), but it will do the
formatting job for you. So, just provide the IDs as strings.

*TIP: keep all template-related sheets in the same document ([Data Catalog Sample Tag Template][7] for reference).*

### 5.3. e2e tests

- pytest

```bash
export GOOGLE_CLOUD_TEST_PROJECT_ID=PROJECT_ID

pytest tests_e2e/load_template_google_sheets_test.py
```

- docker

```bash
docker build --rm --tag gcp-datacatalog-python .
docker run --rm --tty \
  --env GOOGLE_CLOUD_TEST_PROJECT_ID=PROJECT_ID \
  gcp-datacatalog-python \
  pytest tests_e2e/load_template_google_sheets_test.py
```

### 5.4. load_template_google_sheets.py

- python

```bash
python load_template_google_sheets.py \
  --template-id TEMPLATE_ID --display-name DISPLAY_NAME \
  --project-id PROJECT_ID --spreadsheet-id SPREADSHEET_ID \
  [--delete-existing]
```

- docker

```bash
docker build --rm --tag gcp-datacatalog-python .
docker run --rm --tty gcp-datacatalog-python \
  python load_template_google_sheets.py \
  --template-id TEMPLATE_ID --display-name DISPLAY_NAME \
  --project-id PROJECT_ID --spreadsheet-id SPREADSHEET_ID \
  [--delete-existing]
```

[1]: https://cloud.google.com/data-catalog
[2]: https://circleci.com/gh/ricardolsmendes/gcp-datacatalog-python.svg?style=svg
[3]: https://circleci.com/gh/ricardolsmendes/gcp-datacatalog-python
[4]: https://medium.com/google-cloud/data-catalog-hands-on-guide-a-mental-model-dae7f6dd49e
[5]: https://medium.com/google-cloud/data-catalog-hands-on-guide-search-get-lookup-with-python-82d99bfb4056
[6]: https://medium.com/google-cloud/data-catalog-hands-on-guide-templates-tags-with-python-c45eb93372ef
[7]: https://docs.google.com/spreadsheets/d/1DoILfOD_Fb1r5otEz2CUH8SKGkyV5juLakGODTTfOjY
