# image-analysis-GBM

<a href="https://github.com/stepien-lab/image-analysis-GBM/"><img src="https://img.shields.io/badge/GitHub-stepien--lab/image--analysis--GBM-blue" /></a>  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>

The code contained in the image-analysis-GBM project was developed for image analysis of fluorescent images of brain tissue in a glioma-bearing mouse (such as Figure 3 in [this paper](https://doi.org/10.1007/s00285-023-02027-y)).

## Programs
### CellProfiler
[CellProcessing.cpproj](CellProcessing.cpproj) is developed for image analysis with [CellProfiler](https://cellprofiler.org).

**Inputs:**
+ Images with fluorescent labels marking CD3+ (white), CCR2+ (red), and CX3CR1+ (green) cells.
  + Viable cells are denoted by the blue fluorescent label
  + T cells are identified as CD3+ cells (blue and white)
  + MDSCs are identified as CCR2+ and CXC3R1+ (blue, red, and green)
  + Cancer cells are identified as viable cells that are not T cells or MDSCs (blue, but not white, red, or green).

**Outputs:**
+ `.csv` files in a `Data` folder with the spatial (x,y) location of each T cell, MDSC, and cancer cell
+ `.tiff` files in a `ProcessedImages` folder illustrating which cells are identified from each fluorescent marker

### Python
The remaining code is developed in Python for analyzing output from CellProfiler.

It is based on code available from [https://github.com/JABull1066/ExtendedCorrelationFunctions](https://github.com/JABull1066/ExtendedCorrelationFunctions).

## Lead Developer
The lead developer of this code is [Gillian Carr](https://github.com/gilliancarr).

## Licensing
Copyright 2023-2025 [Tracy Stepien's Research Lab Group](https://github.com/stepien-lab/). This is free software made available under the MIT License. For details see the [LICENSE](LICENSE) file.
