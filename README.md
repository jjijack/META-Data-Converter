# META Data Converter

## Overview
This repository provides tools for converting data from [META3.1EXP DT](https://www.aviso.altimetry.fr/en/data/products/value-added-products/global-mesoscale-eddy-trajectory-product/meta3-1-exp-dt.html) into labeled outputs compatible with **EddyNet**, a deep learning model designed for eddy detection.

The input data is sourced from sea surface height datasets provided by [Copernicus](https://data.marine.copernicus.eu/product/SEALEVEL_GLO_PHY_L4_MY_008_047).

---

## Usage Instructions

1. **Input Preparation**  
   Place the downloaded **META3.1EXP DT** dataset in the root directory alongside all provided scripts.

2. **Script Execution Workflow**  
   The generated outputs will be stored in the `Data` folder. Each script is tailored to process either *anticyclonic* or *cyclonic* eddies, indicated by the following suffixes:  
   - **`ac`**: For anticyclonic eddies  
   - **`c`**: For cyclonic eddies  

3. **Execution Order**  
   Execute the scripts with the same suffix in the following order:  
   - `area_limit`  
   - `grid_trans`  
   - `data_generate`  

   - For test datasets in the `grid_trans` step, an additional suffix `test` is included.
   - To output data as a dictionary instead of an array, use `data_generate_dict`.

---

This pipeline ensures accurate and efficient conversion of eddy data for use with EddyNet.
