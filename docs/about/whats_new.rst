.. _whats_new:

What's New
==========

v1.1.15 Minion Party Hangover (1 December 2016)
-----------------------------------------------

  - Fixed a data loading issue when reading HDF4_EOS datasets.

v1.1.14 Minion Party (30 November 2016)
---------------------------------------

  - Added support for buffering/padding of GridWorkflow tile searches

  - Improved the Query class to make filtering by a source or parent dataset easier.
    For example, this can be used to filter Datasets by Geometric Quality Assessment (GQA).
    Use `source_filter` when requesting data.

  - Additional data preparation and configuration scripts

  - Various fixes for single point values for lat, lon & time searches

  - Grouping by solar day now overlays scenes in a consistent, northern scene takes precedence manner.
    Previously it was non-deterministic which scene/tile would be put on top.

v1.1.13 Black Goat (15 November 2016)
-------------------------------------

  - Added support for accessing data through `http` and `s3` protocols

  - Added `dataset search` command for filtering datasets (lists `id`, `product`, `location`)

  - `ingestion_bounds` can again be specified in the ingester config

  - Can now do range searches on non-range fields (e.g. `dc.load(orbit=(20, 30)`)

  - Merged several bug-fixes from CEOS-SEO branch

  - Added Polygon Drill recipe to :ref:`recipes`

v1.1.12 Unnamed Unknown (1 November 2016)
-----------------------------------------

  - Fixed the affine deprecation warning

  - Added `datacube metadata_type` cli tool which supports `add` and `update`

  - Improved `datacube product` cli tool logging

v1.1.11 Unnamed Unknown (19 October 2016)
-----------------------------------------

  - Improved ingester task throughput when using distributed executor

  - Fixed an issue where loading tasks from disk would use too much memory

  - :meth:`.model.GeoPolygon.to_crs` now adds additional points (~every 100km) to improve reprojection accuracy

v1.1.10 Rabid Rabbit (5 October 2016)
-------------------------------------

  - Ingester can now be configured to have WELD/MODIS style tile indexes (thanks Chris Holden)

  - Added --queue-size option to `datacube ingest` to control number of tasks queued up for execution

  - Product name is now used as primary key when adding datasets.
    This allows easy migration of datasets from one database to another

  - Metadata type name is now used as primary key when adding products.
    This allows easy migration of products from one database to another

  - :meth:`.DatasetResource.has` now takes dataset id insted of :class:`.model.Dataset`

  - Fixed an issues where database connections weren't recycled fast enough in some cases

  - Fixed an issue where :meth:`.DatasetTypeResource.get` and :meth:`.DatasetTypeResource.get_by_name`
    would cache `None` if product didn't exist


v1.1.9 Pest Hippo (20 September 2016)
-------------------------------------

  - Added origin, alignment and GeoBox-based methods to :class:`.model.GridSpec`

  - Fixed satellite path/row references in the prepare scripts (Thanks to Chris Holden!)

  - Added links to external datasets in :ref:`indexing`

  - Improved archive and restore command line features: `datacube dataset archive` and `datacube dataset restore`

  - Improved application support features

  - Improved system configuration documentation


v1.1.8 Last Mammoth (5 September 2016)
--------------------------------------

  - :meth:`.GridWorkflow.list_tiles` and :meth:`.GridWorkflow.list_cells` now
    return a :class:`.Tile` object

  - Added `resampling` parameter to :meth:`.Datacube.load` and :meth:`.GridWorkflow.load`. Will only be used if the requested data requires resampling.

  - Improved :meth:`.Datacube.load` `like` parameter behaviour. This allows passing in a :class:`xarray.Dataset` to retrieve data for the same region.

  - Fixed an issue with passing tuples to functions in Analytics Expression Language

  - Added a :ref:`user_guide` section to the documentation containing useful code snippets

  - Reorganized project dependencies into required packages and optional 'extras'

  - Added `performance` dependency extras for improving run-time performance

  - Added `analytics` dependency extras for analytics features

  - Added `interactive` dependency extras for interactivity features


v1.1.7 Bit Shift (22 August 2016)
---------------------------------

  - Added bit shift and power operators to Analytics Expression Language

  - Added `datacube product update` which can be used to update product definitions

  - Fixed an issue where dataset geo-registration would be ignored in some cases

  - Fixed an issue where Execution Engine was using dask arrays by default

  - Fixed an issue where int8 data could not sometimes be retrieved

  - Improved search and data retrieval performance


v1.1.6 Lightning Roll (8 August 2016)
-------------------------------------

  - Improved spatio-temporal search performance. `datacube system init` must be run to benefit

  - Added `info`, `archive` and `restore` commands to `datacube dataset`

  - Added `product-counts` command to `datacube-search` tool

  - Made Index object thread-safe

  - Multiple masking API improvements

  - Improved database Index API documentation

  - Improved system configuration documentation


v1.1.5 Untranslatable Sign (26 July 2016)
-----------------------------------------

  - Updated the way database indexes are patitioned. Use `datacube system init --rebuild` to rebuild indexes

  - Added `fuse_data` ingester configuration parameter to control overlaping data fusion

  - Added `--log-file` option to `datacube dataset add` command for saving logs to a file

  - Added index.datasets.count method returning number of datasets matching the query


v1.1.4 Imperfect Inspiration (12 July 2016)
-------------------------------------------

  - Improved dataset search performance

  - Restored ability to index telemetry data

  - Fixed an issue with data access API returning uninitialized memory in some cases

  - Fixed an issue where dataset center_time would be calculated incorrectly

  - General improvements to documentation and usablity


v1.1.3 Speeding Snowball (5 July 2016)
--------------------------------------

  - Added framework for developing distributed, task-based application

  - Several additional Ingester performance improvements


v1.1.2 Wind Chill (28 June 2016)
--------------------------------

This release brings major performance and usability improvements

  - Major performance improvements to GridWorkflow and Ingester

  - Ingestion can be limited to one year at a time to limit memory usage

  - Ingestion can be done in two stages (serial followed by highly parallel) by using
    --save-tasks/load-task options.
    This should help reduce idle time in distributed processing case.

  - General improvements to documentation.


v1.1.1 Good Idea (23 June 2016)
-------------------------------

This release contains lots of fixes in preparation for the first large
ingestion of Geoscience Australia data into a production version of
AGDCv2.

  - General improvements to documentation and user friendliness.

  - Updated metadata in configuration files for ingested products.

  - Full provenance history is saved into ingested files.

  - Added software versions, machine info and other details of the
    ingestion run into the provenance.

  - Added valid data region information into metadata for ingested data.

  - Fixed bugs relating to changes in Rasterio and GDAL versions.

  - Refactored :class:`GridWorkflow` to be easier to use, and include
    preliminary code for saving created products.

  - Improvements and fixes for bit mask generation.

  - Lots of other minor but important fixes throughout the codebase.


v1.1.0 No Spoon (3 June 2016)
-----------------------------

This release includes restructuring of code, APIs, tools, configurations
and concepts. The result of this churn is cleaner code, faster performance and
the ability to handle provenance tracking of Datasets created within the Data
Cube.

The major changes include:

    - The ``datacube-config`` and ``datacube-ingest`` tools have been
      combined into ``datacube``.

    - Added dependency on ``pandas`` for nicer search results listing and
      handling.

    - :ref:`Indexing <indexing>` and :ref:`ingestion` have been split into
      separate steps.

    - Data that has been :ref:`indexed <indexing>` can be accessed without
      going through the ingestion process.

    - Data can be requested in any projection and will be dynamically
      reprojected if required.

    - **Dataset Type** has been replaced by :ref:`Product <product-definitions>`

    - **Storage Type** has been removed, and an :ref:`Ingestion Configuration
      <ingest-config>` has taken it's place.

    - A new :ref:`datacube-class` for querying and accessing data.


1.0.4 Square Clouds (3 June 2016)
---------------------------------

Pre-Unification release.

1.0.3 (14 April 2016)
---------------------

Many API improvements.

1.0.2 (23 March 2016)
---------------------

1.0.1 (18 March 2016)
---------------------

1.0.0 (11 March 2016)
---------------------

This release is to support generation of GA Landsat reference data.


pre-v1 (end 2015)
-----------------

First working Data Cube v2 code.
