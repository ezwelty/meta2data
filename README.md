# Metadata-driven data development (demo)

This repository demonstrates a metadata-driven approach to dataset development. The goal is to:

* Describe the data with machine-actionable metadata
* Test that the data is as described
* Build derivative products like documentation and spreadsheet templates

This is the general approach I use to maintain glacier datasets like [`fog`](https://wgms.ch/data_databaseversions/), [`glathida`](https://gitlab.com/wgms/glathida), and [`glenglat`](https://github.com/mjacqu/glenglat). I have also written two Python packages to help implement this process: [`tablecloth`](https://github.com/ezwelty/tablecloth), to generate spreadsheet templates from a dataset description, and [`validator`](https://github.com/ezwelty/validator), to write complex data transformation and validation pipelines. For example for the complex [`fog`](https://wgms.ch/data_databaseversions/) dataset, the [metadata](https://gitlab.com/wgms/fog/-/blob/77d2895cf8b95a631520877f1582a62c4f1bb015/src/fog/metadata) is used to generate a [Google Sheets spreadsheet](https://docs.google.com/spreadsheets/d/1o9b2fMuTYWz22-4sRBS0AcxLcGCEF9sdg2rIQfR4muo) for data submission, define the basic [checks](https://gitlab.com/wgms/fog/-/blob/77d2895cf8b95a631520877f1582a62c4f1bb015/src/fog/schema.py#L706) used to validate submissions, and render [documentation templates](https://gitlab.com/wgms/fog/-/blob/77d2895cf8b95a631520877f1582a62c4f1bb015/src/fog/templates) to produce e.g., the final [readme](https://wgms.ch/downloads/WGMS_DOI_2025-02.pdf).

The following files are the foundation of this demonstration dataset:

- `data/*.csv` – Tabular data (CSV)
- `datapackage.yaml` – Metadata describing the data (YAML following the [Data Package](https://datapackage.org/standard/data-package) specification)
- `tests/test_*.py` – Tests placing further constraints on the data ([`pytest`](https://docs.pytest.org))
- `environment.yaml` – Python environment definition ([`conda`](https://docs.conda.io))

Additional files are used to build derivative products (written to the `build/` directory):

- `templates/*.jinja` – Documentation templates ([`Jinja`](https://jinja.palletsprojects.com))
- `functions.py` – Functions to build documentation and spreadsheet templates

## Installation

Either [download](https://github.com/ezwelty/meta2data/archive/refs/heads/main.zip) and unzip this repository, or clone it using `git`.

```bash
git clone https://github.com/ezwelty/meta2data
```

Start a shell session, change to the `meta2data` directory created above, and install the Python environment defined in `environment.yaml` (using [`conda`](https://docs.conda.io)).

```bash
cd meta2data
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

Write the template to `build/template.xlsx`.

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

Render the template (`templates/readme.html.jinja`) with content from the metadata (`datapackage.yaml`) and write the result to `build/readme.html`.

```bash
python functions.py build_readme
```
