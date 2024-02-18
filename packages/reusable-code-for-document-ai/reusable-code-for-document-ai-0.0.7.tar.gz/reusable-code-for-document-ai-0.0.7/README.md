## Instructions

## Build and Push the packages on Artifact Registry
#### Install required packages

To install the required packages, execute the following command::

```shell
pip install -r requirements.txt
```

#### Create a repository
Run the following command to create a new Python package repository in the current project named `reusable-code-for-document-ai` in the location `us-central1`.

```shell
gcloud artifacts repositories create reusable-code-for-document-ai \
    --repository-format=python \
    --location=us-central1 \
    --description="Python package repository"
```

Run the following command to verify that your repository was created:

```shell
gcloud artifacts repositories list
```

#### Update Code

If you want to update the code, please make changes inside the `reusable_code` folder.

### Build python package

`build_package.sh` script automates the installation of required pip packages and the build process for a Python package.

##### Prerequisites:
**Python3** should be installed on the system

##### Notes:
1. Delete the `dist` folder if it already exists.
2. Make sure to run the script in a directory where you have appropriate write permissions, as the build process may generate files in the current directory.

##### Usage:
1. Open a terminal or command prompt
2. Navigate to the directory where the bash script is located.
3. Update the version number in the `setup.cfg` file before uploading the package.
4. Execute the bash script using the following command:

Give execute permission to your script

```shell
chmod +x build_package.sh
```
And to run your script
```shell
./build_package.sh
```

This script build the Python package using the `python3 -m build` command. This step generates the distribution files for the package.
After run this bash script you will see this script create a `dist` directory

### Upload the package to the repository

Upload the packages to the repository from your `dist` directory

```shell
twine upload --repository-url https://us-central1-python.pkg.dev/saifuls-playground/reusable-code-for-document-ai/ --verbose dist/*
```


## Installing process
Following instructions will guide you through setting up the keyring library and configuring it to work with the Rebuy Product API.

**Note:** If you are trying to install it on a local machine, run ``gcloud init`` before starting

### Setting up keyring

1. Start by updating the package list using
``` shell
sudo apt update -y
```

2. The following command to install pip for Python 3
```shell
sudo apt install python3-pip -y
```

3. Install the keyring library
``` shell
pip install keyring
```
4. Install the Artifact Registry backend

Artifact Registry backend is required for authentication with the Rebuy Product API. Install it by running the following command:
``` shell
pip install keyrings.google-artifactregistry-auth
```
### Installing

5. Install using `pip` command

Use the pip command to install this package:

```shell
pip install -i https://us-central1-python.pkg.dev/saifuls-playground/reusable-code-for-document-ai/simple/ reusable-code-for-document-ai
```


## Basic Usage

```
from reusable_code.process_document import CustomGoogleDocAIProcessor

processor = GoogleDocAIProcessor(
    location="your_location",
    processor_name="your_processor_name",
    processor_options=your_processor_options
)

document = processor.process_document("path_to_your_document")

```

Make sure to replace `your_location`, `your_processor_name`, `your_processor_options`, and `path_to_your_document` with appropriate values.

#### Reference
1. [Store Python packages in Artifact Registry](https://cloud.google.com/artifact-registry/docs/python/store-python)
2. [Set up authentication to Python package repositories](https://cloud.google.com/artifact-registry/docs/python/authentication)

