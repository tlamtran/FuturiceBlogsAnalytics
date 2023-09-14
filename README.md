# Futurice Blogs Analytics - Data science project

This repository contains the code and resources for a data science project conducted on behalf of Futurice. The project aims to analyze blogs created by Futurice.

You can find slides of our final presentation in this repo! 

## Project Directory Structure

The project directory is organized as follows:

- **data/**: This directory is used to store both raw and processed data.
  - `raw/`: Contains raw, unaltered data files.
  - `processed/`: Contains cleaned, transformed, and preprocessed data.

- **notebooks/**: Jupyter notebooks for exploratory stuff such as data analysis and visualization.

- **src/**: Python source code for data preprocessing, modeling, and other functions.
  
- **results/**: This directory is for storing model checkpoints, plots, and other results.

- **environment.yml**: Specifies the Python environment and dependencies required for the project. Use `conda` to create this environment.

- **README.md**: This file, providing an overview of the project structure and instructions for setup and usage.


## Getting Started

Follow these steps to set up and run the project locally:

1. Clone this repository:
   1. `git clone https://github.com/tlamtran/FuturiceBlogsAnalytics`
2. Conda is recommended to easily install all the dependencies in an isolated manner:
   1. `conda env create -f environment.yml` (This might take a while)
   2. `conda activate futurice-blogs-env`