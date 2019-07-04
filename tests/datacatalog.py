import os
import pytest

from google.api_core.exceptions import PermissionDenied
from google.cloud import datacatalog_v1beta1

from .bigquery import table

TEST_PROJECT_ID = os.environ['GOOGLE_CLOUD_TEST_PROJECT_ID']

datacatalog_client = datacatalog_v1beta1.DataCatalogClient()


@pytest.fixture
def tag_template(scope='function'):
    location = datacatalog_client.location_path(TEST_PROJECT_ID, 'us-central1')

    # Delete a Tag Template with the same name if it already exists.
    try:
        datacatalog_client.delete_tag_template(
            name=f'{location}/tagTemplates/quickstart_test_tag_template', force=True)
    except PermissionDenied:
        pass

    template = datacatalog_v1beta1.types.TagTemplate()
    template.fields['boolean_field'].type.primitive_type = \
        datacatalog_v1beta1.enums.FieldType.PrimitiveType.BOOL
    template.fields['double_field'].type.primitive_type = \
        datacatalog_v1beta1.enums.FieldType.PrimitiveType.DOUBLE
    template.fields['string_field'].type.primitive_type = \
        datacatalog_v1beta1.enums.FieldType.PrimitiveType.STRING
    template.fields['timestamp_field'].type.primitive_type = \
        datacatalog_v1beta1.enums.FieldType.PrimitiveType.TIMESTAMP

    template.fields['enum_field'].type.enum_type.allowed_values.add().display_name = 'VALUE 1'
    template.fields['enum_field'].type.enum_type.allowed_values.add().display_name = 'VALUE 2'

    tag_template = datacatalog_client.create_tag_template(
        parent=location, tag_template_id='quickstart_test_tag_template', tag_template=template)

    yield tag_template

    datacatalog_client.delete_tag_template(tag_template.name, force=True)


@pytest.fixture
def table_entry(table, scope='function'):
    entry = datacatalog_client.lookup_entry(
        linked_resource=f'//bigquery.googleapis.com/projects/{TEST_PROJECT_ID}'
                        f'/datasets/quickstart_test_dataset/tables/quickstart_test_table_2')

    yield entry


@pytest.fixture
def tag(table_entry, tag_template, scope='function'):
    tag = datacatalog_v1beta1.types.Tag()
    tag.template = tag_template.name

    tag.fields['boolean_field'].bool_value = True
    tag.fields['double_field'].double_value = 10.5
    tag.fields['string_field'].string_value = 'test'
    tag.fields['timestamp_field'].timestamp_value.FromJsonString('2019-07-04T01:00:30Z')
    tag.fields['enum_field'].enum_value.display_name = 'VALUE 1'

    tag = datacatalog_client.create_tag(parent=table_entry.name, tag=tag)

    yield tag

    datacatalog_client.delete_tag(tag.name)
