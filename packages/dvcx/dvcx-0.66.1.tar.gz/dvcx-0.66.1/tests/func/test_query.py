from textwrap import dedent

import dill

from dql.cli import query
from dql.query import C, DatasetQuery


def test_query(cloud_test_catalog_tmpfile, tmp_path, capsys):
    catalog = cloud_test_catalog_tmpfile.catalog
    src_uri = cloud_test_catalog_tmpfile.src_uri

    catalog_info = {
        "catalog_init_params": catalog.get_init_params(),
        "id_generator_params": catalog.id_generator.clone_params(),
        "metastore_params": catalog.metastore.clone_params(),
        "warehouse_params": catalog.warehouse.clone_params(),
    }
    catalog_info_filepath = tmp_path / "catalog-info"
    with open(catalog_info_filepath, "wb") as f:
        dill.dump(catalog_info, f)

    query_script = f"""\
    import dill
    from dql.catalog import Catalog

    catalog_info_filepath = {str(catalog_info_filepath)!r}
    with open(catalog_info_filepath, "rb") as f:
        catalog_info = dill.load(f)
    (
        id_generator_class,
        id_generator_args,
        id_generator_kwargs,
    ) = catalog_info["id_generator_params"]
    id_generator = id_generator_class(*id_generator_args, **id_generator_kwargs)
    (
        metastore_class,
        metastore_args,
        metastore_kwargs,
    ) = catalog_info["metastore_params"]
    metastore = metastore_class(*metastore_args, **metastore_kwargs)
    (
        warehouse_class,
        warehouse_args,
        warehouse_kwargs,
    ) = catalog_info["warehouse_params"]
    warehouse = warehouse_class(*warehouse_args, **warehouse_kwargs)
    catalog = Catalog(
        id_generator=id_generator,
        metastore=metastore,
        warehouse=warehouse,
        **catalog_info["catalog_init_params"],
    )

    from dql.query import C, DatasetQuery

    DatasetQuery({src_uri!r}, catalog=catalog)
    """
    query_script = dedent(query_script)

    filepath = tmp_path / "query_script.py"
    filepath.write_text(query_script)

    ds_name = "my-dataset"
    dataset = query(catalog, str(filepath), ds_name)
    captured = capsys.readouterr()
    assert captured.out == "Registered dataset: my-dataset@v1\n"
    assert captured.err == ""
    assert (dataset.name, dataset.latest_version) == (ds_name, 1)

    result = (
        DatasetQuery(src_uri, catalog=catalog)
        .select(C.source, C.parent, C.name, C.vtype, C.size)
        .order_by(C.source, C.parent, C.name)
        .to_records()
    )

    assert result == [
        {
            "source": src_uri,
            "parent": "",
            "name": "description",
            "vtype": "",
            "size": 13,
        },
        {
            "source": src_uri,
            "parent": "cats",
            "name": "cat1",
            "vtype": "",
            "size": 4,
        },
        {
            "source": src_uri,
            "parent": "cats",
            "name": "cat2",
            "vtype": "",
            "size": 4,
        },
        {
            "source": src_uri,
            "parent": "dogs",
            "name": "dog1",
            "vtype": "",
            "size": 4,
        },
        {
            "source": src_uri,
            "parent": "dogs",
            "name": "dog2",
            "vtype": "",
            "size": 3,
        },
        {
            "source": src_uri,
            "parent": "dogs",
            "name": "dog3",
            "vtype": "",
            "size": 4,
        },
        {
            "source": src_uri,
            "parent": "dogs/others",
            "name": "dog4",
            "vtype": "",
            "size": 4,
        },
    ]
