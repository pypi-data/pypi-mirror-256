# Cloud Optimized GeoTiff Generator

## Overview
This package wrapped around the native GDAL library enables Cloud Optimized GeoTiffs generation at ease into your Python projects.

## Installation
You can install the package via pip:
```bash
pip install cog_generation
```

To generate a cog:

```python
from cog_generator import generate_cog
input_tif_list = ["sample1.tif", "sample2.tif"]
output_tif_path = "output_cog.tif"
options = {"compress": "lzw", "level": 9}

message, status_code = generate_cog(input_tif_list, output_tif_path, options)
```


## Parameters available for options

- **compress**: Defaults to `lzw`. Options include `none`, `lzw`, `jpeg`, `deflate`, `zstd`, `webp`, `lerc`, `lerc_deflate`, `lerc_zstd`, `lzma`.

- **level**: Defaults to `6` for DEFLATE/LZMA, `9` for ZSTD. Compression level options depend on the compression type. Lower values result in faster compression but less efficient compression rate. 1 is the fastest.

- **QUALITY**: Defaults to `75`. JPEG/WEBP quality setting. For WEBP, `QUALITY=100` automatically turns on lossless mode.

- **num_threads**: Defaults to `all_cpus`. Enable multi-threaded compression by specifying the number of worker threads.

- **PREDICTOR**: Defaults to `NO`. Set the predictor for LZW, DEFLATE, and ZSTD compression.

- **bigtiff**: Defaults to `IF_NEEDED`. Control whether the created file is a BigTIFF or a classic TIFF.

- **zoom_level**: (GDAL >= 3.5) Zoom level number (starting at 0 for coarsest zoom level).

