# Market Coverage Dashboard
This project hosts the entire codebase (incl. datasets) for the creation of a Market Review / Market Coverage Dashboard in the context of the Venture Capital Industry.
This repository contains all neccessary information to trace and reproduce the data analysis, data processing, data enrichment and visualizations.

Please note that some services and scripts require API keys to external services. In addition, this project leverages a PostgreSQL database hosted on GCP.
The respective credentials are available upon request. 

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