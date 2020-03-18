# Dataverse Sample Data

Populate your Dataverse installation with sample data.

## Requirements

- Python 3.4 or higher

## Installation

Clone this repo.

    git clone https://github.com/IQSS/dataverse-sample-data.git

Change directories into the repo that you cloned.

    cd dataverse-sample-data

Create a virtual environment for this project.

    python3 -m venv venv

Activate the virtual environment you just created.

    source venv/bin/activate

Install dependencies into the virtual environment, especially [pyDataverse][].

    pip install -r requirements.txt

Copy `dvconfig.py.sample` to `dvconfig.py` (see the `cp` command below) and add your API token (using your favorite text editor, which may not be `vi` as shown below). Note that the config file specifies which sample data will be created.

    cp dvconfig.py.sample dvconfig.py
    vi dvconfig.py

## Adding sample data

Assuming you have already run the `source` and `cd` commands above, you should be able to run the following command to create sample data.

    python create_sample_data.py

All of the steps above may be automated in a fresh installation of Dataverse on an EC2 instance on AWS by downloading [ec2-create-instance.sh][] and [main.yaml][]. Edit main.yml to set `dataverse.sampledata.enabled: true` and adjust any other settings to your liking, then execute the script with the config file like this:

    curl -O https://raw.githubusercontent.com/IQSS/dataverse-ansible/master/ec2/ec2-create-instance.sh
    chmod 755 ec2-create-instance.sh
    ./ec2-create-instance.sh -g main.yml

For more information on spinning up Dataverse in AWS (especially if you don't have the `aws` executable installed), see http://guides.dataverse.org/en/latest/developers/deployment.html

## Contributing

We love contributors! Please see our [Contributing Guide][] for ways you can help.

[ec2-create-instance.sh]: https://github.com/IQSS/dataverse-ansible/blob/master/ec2/ec2-create-instance.sh
[ec2config.yaml]: https://raw.githubusercontent.com/IQSS/dataverse-ansible/master/defaults/main.yml
[Contributing Guide]: CONTRIBUTING.md
[pyDataverse]: https://pypi.org/project/pyDataverse/
