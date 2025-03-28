import frictionless

package = frictionless.Package('datapackage.yaml')
dfs = {
  resource.name: resource.to_pandas().reset_index()
  for resource in package.resources
}


def test_borehole_id_is_sorted() -> None:
  """Test that borehole is sorted by id."""
  assert dfs['borehole']['id'].is_monotonic_increasing


def test_measurement_date_on_or_after_borehole_date() -> None:
  """Test that measurement date is on or after borehole date."""
  df = dfs['measurement']
  borehole_date = dfs['borehole'].set_index('id')['date'].loc[df['borehole_id']].values
  assert df['date'].ge(borehole_date).all()
