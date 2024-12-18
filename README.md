# Market Coverage Dashboard
This project hosts the entire codebase (incl. datasets) for the creation of a Market Review / Market Coverage Dashboard in the context of the Venture Capital Industry.
This repository contains all necessary information to trace and reproduce the data analysis, data processing, data enrichment, and visualizations.

Please note that some services and scripts require API keys to external services. In addition, this project leverages a PostgreSQL database hosted on GCP.
The respective credentials are available upon request. 

### Repository Structure
The repository is organized as follows:
```
/data                    # Contains all datasets used for analysis and processing
/db                      # All relevant scripts and configurations of the database
/eda_and_preprocessing   # Jupyter notebooks for EDA and Python class for Preprocessing
/enrichment-ml           # Scripts to enrich the data with Machine Learning techniques
/enrichment-apis         # Scripts to enrich the data with external APIs
/utils                   # Helper functions for various purposes
.env.sample              # Sample environment variables file
README.md                # Project documentation
requirements.txt         # Python dependencies
```

Before starting to execute any code, please make sure to follow these steps:

### Set up venv environment
```bash
python -m venv .venv
pip install -r pip_requirements.txt
```

### Activate your venv environment
```bash
source .venv/bin/activate
```

### Set up environment variables
* duplicate the '.env.sample' file
* rename that file to '.env'
* add the relevant required credentials