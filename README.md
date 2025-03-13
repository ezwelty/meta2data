# Metadata-driven data development

This repository demonstrates a metadata-driven approach to data development. The goal is to:

* Describe the data with machine-actionable metadata
* Test that the data is as described
* Generate spreadsheet templates
* Generate documentation

The following files are the foundation of our dataset:

- `data/*.csv` – Tabular data (CSV)
- `datapackage.yaml` – Metadata describing the data (YAML following the [Data Package](https://datapackage.org/standard/data-package) specification)
- `tests/test_*.py` – Tests placing further constraints on the data ([`pytest`](https://docs.pytest.org))
- `environment.yaml` – Python environment definition ([`conda`](https://docs.conda.io))

Additional files are used to build derivative products (written to the `build` directory):

- `templates/*.jinja` – Documentation templates ([`Jinja`](https://jinja.palletsprojects.com))
- `functions.py` – Functions to build documentation and spreadsheet templates


## Installation

Install the Python environment defined in `environment.yaml` (using [`conda`](https://docs.conda.io)).

```bash
conda env create --file environment.yaml
conda activate meta2data
```

## Testing

Validate the data package described in `datapackage.yaml` (using [`frictionless-py`](https://framework.frictionlessdata.io)).

```bash
frictionless validate datapackage.yaml
```

Run additional tests (using [`pytest`](https://docs.pytest.org)).

```bash
pytest
```

## Spreadsheet templates

Generate spreadsheet templates from the metadata (`datapackage.yaml`).

### Microsoft Excel

```bash
python functions.py build_excel_template
```

### Google Sheets

Access to Google Sheets requires a Google Cloud project service
account key (https://pygsheets.readthedocs.io/en/stable/authorization.html#service-account).
Copy the example environment file:

```bash
cp .env.example .env
```

and add your key.
Optionally, add your Google account email so that Google Sheets created by the
service account are shared with you.
Finally:

```bash
python functions.py build_gsheets_template --name 'template'
```

## Documentation

Render the template (`templates/readme.html.jinja`) with content from the metadata (`datapackage.yaml`), and write the result to `build/readme.html`.

```bash
python functions.py build_readme
```
