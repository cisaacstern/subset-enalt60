import gcsfs
from fsspec.implementations.local import LocalFileSystem
from pangeo_forge_recipes.storage import MetadataTarget, CacheFSSpecTarget


def setup_logging():
    import logging
    import sys
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("pangeo_forge_recipes")
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)


def setup_targets(recipe_dict, key):
    """Wrapping this in a function so we can reuse it after restarting the kernel
    """
    fs_gcs = gcsfs.GCSFileSystem(anon=True,)
    fs_local = LocalFileSystem()

    cache_base = 'gs://pangeo-forge-us-central1/pangeo-forge-cache/swot_adac'

    rec = recipe_dict[key]

    rec.input_cache = CacheFSSpecTarget(fs_gcs, f"{cache_base}/{key}")
    rec.metadata_cache = MetadataTarget(fs_local, f"metadata/{key.replace('/', '-')}")
    rec.target = MetadataTarget(fs_local, f"zarr_build/{key.replace('/', '-')}.zarr")

    print(f"""Targets for recipe_dict["{key}"] set to:

    input_cache: {rec.input_cache.root_path}
    metadata_cache: {rec.metadata_cache.root_path}
    target: {rec.target.root_path}
    """)

    return rec
