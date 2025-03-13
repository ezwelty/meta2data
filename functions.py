import os
from pathlib import Path
import yaml

import dotenv
import jinja2
import pygsheets
import tablecloth.excel
import tablecloth.gsheets

dotenv.load_dotenv()


METADATA_PATH = Path('datapackage.yaml')
BUILD_DIR = Path('build')


def render_header_comments(metadata: dict) -> dict[str, list[str]]:
  """Render header comments from metadata."""
  # Read template from file
  template_path = Path('templates/header-comment.jinja')
  template: jinja2.Template = jinja2.Template(
    source=template_path.read_text(), trim_blocks=True, lstrip_blocks=True
  )
  # Render template for each column and table
  return {
    resource['name']: [
      template.render(**field) for field in resource['schema']['fields']
    ]
    for resource in metadata['resources']
  }


def build_readme() -> None:
  """Build a README file from a template and metadata."""
  # Read metadata from file
  metadata = yaml.safe_load(METADATA_PATH.read_text())
  # Read template from file
  template_path = Path('templates/readme.html.jinja')
  template: jinja2.Template = jinja2.Template(
    source=template_path.read_text(), trim_blocks=True, lstrip_blocks=True
  )
  # Render template and write to file
  text = template.render(**metadata)
  BUILD_DIR.mkdir(exist_ok=True)
  BUILD_DIR.joinpath('readme.html').write_text(text)


def build_excel_template() -> None:
  """Build an Excel template from a metadata file."""
  # Read metadata from file
  metadata = yaml.safe_load(METADATA_PATH.read_text())
  # Render header comments
  header_comments = render_header_comments(metadata)
  # Render and write template to file
  BUILD_DIR.mkdir(exist_ok=True)
  tablecloth.excel.write_template(
    metadata, path=BUILD_DIR.joinpath('template.xlsx'), header_comments=header_comments
  )


def build_gsheets_template(name: str) -> str:
  """
  Build a Google Sheets template from a metadata file.

  Args:
    name: Spreadsheet name.

  Returns:
    URL of the created spreadsheet.

  Raises:
    ValueError: If the GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY environment variable is
      missing or if a spreadsheet by that name already exists.
  """
  if not os.getenv('GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY'):
    raise ValueError('Missing GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY')
  # Authenticate with Google Sheets
  client = pygsheets.authorize(
    service_account_env_var='GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY'
  )
  try:
    client.open(name)
    raise ValueError(f"Spreadsheet '{name}' already exists")
  except pygsheets.SpreadsheetNotFound:
    pass
  # Create a new spreadsheet
  book = client.create(name)
  if os.getenv('GOOGLE_ACCOUNT'):
    book.share(os.getenv('GOOGLE_ACCOUNT'), role='writer', type='user')
  # Read metadata from file
  metadata = yaml.safe_load(METADATA_PATH.read_text())
  # Render header comments
  header_comments = render_header_comments(metadata)
  # Render and write template to file
  tablecloth.gsheets.write_template(
    metadata, book=book, header_comments=header_comments
  )
  return f'https://docs.google.com/spreadsheets/d/{book.id}'


if __name__ == '__main__':
  # Expose functions to command line
  import fire
  fire.Fire({
    'build_readme': build_readme,
    'build_excel_template': build_excel_template,
    'build_gsheets_template': build_gsheets_template,
  })
