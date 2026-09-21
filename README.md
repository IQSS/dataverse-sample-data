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

    pip3 install -r requirements.txt

Copy `dvconfig.py.sample` to `dvconfig.py` (see the `cp` command below) and add your API token (using your favorite text editor, which may not be `vi` as shown below). Note that the config file specifies which sample data will be created.

    cp dvconfig.py.sample dvconfig.py
    vi dvconfig.py

Note that the environment variable `$API_TOKEN` will override `api_token` in `dvconfig.py`.

## (Optional) Adding a custom dataset with specific number of files

You can add a specific number of files to the dataset "Dataverse performance test dataset" with:
    
    python create_sample_custom_dataset.py

You'll be prompted to specify the number of files you wish to create. The application will then generate the requested number of files, each one with the Dataverse logo in a randomly chosen color. These files will be in PNG format. It's important to complete this step before adding any data, as the dataset will otherwise be empty.

If you experience the `OSError: no library called "cairo-2" was found` error please declare the following env variable as documented [here](https://github.com/Kozea/CairoSVG/issues/392#issuecomment-1927435606):

    export DYLD_LIBRARY_PATH="/opt/homebrew/opt/cairo/lib:$DYLD_LIBRARY_PATH"

## (Optional) Big batch dataset ingestion and performance benchmark

For large-scale dataset ingestion and performance testing (e.g. hundreds or thousands of files in batches), you can use `create_sample_big_batch_dataset.py`:

    python create_sample_big_batch_dataset.py --total-files 1000 --batch-size 100 --batch-delay 2.0

Key features:
- **Fast and lightweight:** Generates sample text or minimal GIF files without needing external C libraries (such as CairoSVG / cairo-2).
- **Batch pacing:** Replicates real-world ingestion tools (like DVUploader) with configurable batch sizes and inter-batch delays.
- **Latency & throughput reporting:** Automatically measures upload latency per batch, compares the first 10% vs last 10% of uploads to detect database or indexing degradation, and prints summary statistics.
- **Local generation mode:** Run with `--generate-only` to write files into `./data/dataverses/dataverse-performance-demo/datasets/performance-test/files/` for consumption by `create_sample_data.py`.

Options:
- `--total-files`: Total number of sample files (default: 100)
- `--batch-size`: Batch size before delay (default: 50)
- `--batch-delay`: Delay in seconds between batches (default: 1.0s)
- `--file-type`: `txt` (default), `gif` (minimal 1x1 image), or `mixed`
- `--url`: Dataverse base URL (default: http://localhost:8080 or from `dvconfig.py` / `$DATAVERSE_URL`)
- `--api-token`: API Token (default: from `dvconfig.py` or `$API_TOKEN`)
- `--dataset-id` / `--dataset-pid`: Target dataset ID or PID (creates a dedicated benchmark dataset by default)
- `--generate-only`: Only write files to disk without uploading directly

## Adding sample data

Assuming you have already run the `source` and `cd` commands above, you should be able to run the following command to create sample data.

    python create_sample_data.py

    https://github.com/Kozea/CairoSVG/issues/392#issuecomment-1927435606

    export DYLD_LIBRARY_PATH="/opt/homebrew/opt/cairo/lib:$DYLD_LIBRARY_PATH"

All of the steps above may be automated in a fresh installation of Dataverse on an EC2 instance on AWS by downloading [ec2-create-instance.sh][] and [main.yaml][]. Edit main.yml to set `dataverse.sampledata.enabled: true` and adjust any other settings to your liking, then execute the script with the config file like this:

    curl -O https://raw.githubusercontent.com/GlobalDataverseCommunityConsortium/dataverse-ansible/master/ec2/ec2-create-instance.sh
    chmod 755 ec2-create-instance.sh
    ./ec2-create-instance.sh -g main.yml

For more information on spinning up Dataverse in AWS (especially if you don't have the `aws` executable installed), see http://guides.dataverse.org/en/latest/developers/deployment.html

## Contributing

We love contributors! Please see our [Contributing Guide][] for ways you can help.

[ec2-create-instance.sh]: https://github.com/GlobalDataverseCommunityConsortium/dataverse-ansible/blob/master/ec2/ec2-create-instance.sh
[main.yaml]: https://github.com/GlobalDataverseCommunityConsortium/dataverse-ansible/blob/master/defaults/main.yml
[Contributing Guide]: CONTRIBUTING.md
[pyDataverse]: https://pypi.org/project/pyDataverse/
