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

Change directories into the repo that you cloned.

    cd dataverse-sample-data

Install dependencies into the virtual environment, especially [pyDataverse][].

    pip install -r requirements.txt

Copy `dvconfig.py.sample` to `dvconfig.py` (see the `cp` command below) and add your API token (using your favorite text editor, which may not be `vi` as shown below). Note that the config file specifies which sample data will be created.

    cp dvconfig.py.sample dvconfig.py
    vi dvconfig.py

## Adding sample data

Assuming you have already run the `source` and `cd` commands above, you should be able to run the following command to create sample data.

    python create_sample_data.py

All of the steps above can be automated on an fresh installation of Dataverse on an EC2 instance on AWS by downloading [ec2-create-instance.sh][] and [ec2config.yaml][] and executing the script with the config file like this:

    chmod 755 ec2-create-instance.sh
    ./ec2-create-instance.sh -g ec2config.yaml

For more information on spinning up Dataverse on AWS (especially if you don't have the `aws` executable installed), see http://guides.dataverse.org/en/latest/developers/deployment.html

## Known issues

- Because of how file hierarchy support was implemented (using the [Updating File Metadata][] API endpoint), multiple files with the same name are not supported. The following error is expected: "This file already exists in the dataset."

## Contributing

We love contributors! Please see our [Contributing Guide][] for ways you can help.

[ec2-create-instance.sh]: https://github.com/IQSS/dataverse-ansible/blob/master/ec2/ec2-create-instance.sh
[ec2config.yaml]: ec2config.yaml
[Updating File Metadata]: http://guides.dataverse.org/en/4.15/api/native-api.html#updating-file-metadata
[Contributing Guide]: CONTRIBUTING.md
[pyDataverse]: https://pypi.org/project/pyDataverse/
