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

## Usage in automated processes without API key
Sometimes you don't want to retrieve an API key manually, like at demo times
or when you do automatic deployments of sample data.

For these cases, a script `get_api_token.py` has been added for your convenience.

You can use it like follows (just an example):
```
API_TOKEN=`python get_api_token.py` python create_sample_data.py
```

The script understands two additional environment variables (in addition to
those from `dvconfig.py`):
* `DATAVERSE_USER`
    * Username of the user whos API token we want to retrieve
    * Defaults to `dataverseAdmin`
* `DATAVERSE_PASSWORD`
    * either a cleartext password or a path to a file containing the clear text
      password for the user.
    * Defaults to `admin1` (usable for dataverse-ansible and dataverse-kubernetes)

In case of a successfull retrieval, it will print the password to standard out.
Error will be written to standard error, so you will see it at the top of
a failed attempt to load the data.

Please be aware that you will have to enable
[:AllowApiTokenLookupViaApi](http://guides.dataverse.org/en/latest/installation/config.html#allowapitokenlookupviaapi)
configuration option in your Dataverse to use this script. You can disable
after deploying the data, no harm done.

## Contributing

We love contributors! Please see our [Contributing Guide][] for ways you can help.

[ec2-create-instance.sh]: https://github.com/IQSS/dataverse-ansible/blob/master/ec2/ec2-create-instance.sh
[ec2config.yaml]: https://raw.githubusercontent.com/IQSS/dataverse-ansible/master/defaults/main.yml
[Contributing Guide]: CONTRIBUTING.md
[pyDataverse]: https://pypi.org/project/pyDataverse/
