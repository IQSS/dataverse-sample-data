# Dataverse Sample Data

Populate your Dataverse installation with sample data.

## Requirements

- Python 3.4 or higher

## Installation

Clone this repo.

    git clone https://github.com/IQSS/dataverse-sample-data.git

Create a virtual environment for this project.

    mkdir ~/envs
    python3 -m venv ~/envs/dataverse-sample-data

Activate the virtual environment you just created.

    source ~/envs/dataverse-sample-data/bin/activate

Install dependencies into the virtual environment, especially [pyDataverse][].

    pip install -r requirements.txt

Copy `dvconfig.py.sample` to `dvconfig.py` and add your API token.

## Adding sample data

Create a dataverse.

    python create_dataverse.py

Create a dataset and upload files.

    python create_dataset.py

[pyDataverse]: https://pypi.org/project/pyDataverse/
