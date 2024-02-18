from osgeo import gdal
import os
import sys
import subprocess
import logging

# from .utils import parse_options

# logging
logger = logging.getLogger(__name__)
LOG_LEVEL = logging.INFO
logging.basicConfig(level=LOG_LEVEL)


def parse_options(options):
    opt_params_cmd = ""

    if "compress" in options:
        compress = options["compress"]
        if compress in ["none", "lzw", "jpeg", "deflate", "zstd", "webp", "lerc", "lerc_deflate", "lerc_zstd", "lzma"]:
            opt_params_cmd += f"-co COMPRESS={compress} "
        else:
            raise Exception("Invalid compress params.")
    
    if "level" in options:
        level = options["level"]
        if level in range(1,22):
            opt_params_cmd += f"-co LEVEL={level} "
        else:
            raise Exception("Invalid level params. Should be integer number.")
        
    if "zoom_level" in options:
        zoom_level = options["zoom_level"]
        if zoom_level in range(1, 30):
            opt_params_cmd += f"-co ZOOM_LEVEL={zoom_level} "
        else:
            raise Exception("Invalid zoom_level params. Should be in between 1 and 30.")

    if "num_threads" in options:
        num_threads = options["num_threads"]
        if isinstance(num_threads, int) or num_threads=="all_cpus":
            opt_params_cmd += f"-co NUM_THREADS={zoom_level} "     
        else:
            raise Exception("Invalid num_threads params.")

    if "predictor" in options:
        predictor = options["predictor"]
        if predictor in ["yes", "no", "standard", "floating_point", 2, 3]:
            opt_params_cmd += f"-co PREDICTOR={predictor} " 
        else:
            raise Exception("Invalid predictor params.")
        
    if "bigtiff" in options:
        bigtiff = options["bigtiff"]
        if bigtiff in ["yes", "no", "if_needed", "if_safer"]:
            opt_params_cmd += f"-co BIGTIFF={bigtiff} " 
        else:
            raise Exception("Invalid bigtiff params.")
    
    return opt_params_cmd


def generate_cog(input_tif_list: list, output_tif_path:str, options:dict):
    """
    Configures cog generation config from incoming parameters.

    Arguments
    ---------
    input_tif_list <List>: list of paths of input tiff files.

    output_tif <Str>: path to set for the generated cog.

    options <Dict>: other parameters for the cog generation.
    
    Returns
    -------
    message <str>, status_code <int>: message and status code of the COG generation process.
    """

    logger.info("***************COG Generation started***************")

    if not any([input_tif_list, output_tif_path]):
        return "input_tif_list and output_tif_path are required params", 400

    input_paths = " ".join(input_tif_list)

    if options:
        options_cmd = parse_options(options)
    cmd = f"gdal_translate {input_paths} {output_tif_path} -of COG {options_cmd}"

    logger.info("Running command: " + cmd)

    try:
        cog_generator(cmd)
        logger.info("COG generation successful!")
        return "COG generated successfully", 200
    except Exception as e:
        logger.error(f"Exception | COG Generation Failed. | {str(e)}")
        return f"COG generation failed. Details: {str(e)}", 400

def cog_generator(command):
    subprocess.run(command, shell=True, check=True)