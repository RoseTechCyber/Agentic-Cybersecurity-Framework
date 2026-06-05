# Fabric Adapter (local simulation)

This folder contains guidance for simulating a Microsoft Fabric-like data lake locally using Parquet/Delta files and simple metadata registration.

Strategy
- Use a local folder (data/fabric_lake) to store Parquet files for datasets.
- Maintain a simple YAML/JSON metadata registry describing datasets, schemas, and lineage.
- Provide adapters that read data from the local "fabric" and present it via APIs to the rest of the system.

Example layout
- data/
  - fabric_lake/
    - logs/2026-06-01/*.parquet
    - telemetry/*.parquet
  - metadata/
    - datasets.yaml

Quickstart
1. Create the local lake folder:
   mkdir -p data/fabric_lake
2. Use pandas to write Parquet files as an example:
   import pandas as pd
   df.to_parquet('data/fabric_lake/example.parquet')
3. The adapter can load parquet files and register them in the metadata file.

Next steps
- Implement connectors that transform and copy data into Cosmos DB collections for search and governance.
- Add lineage tracing by recording dataset -> transformation -> output in metadata.
