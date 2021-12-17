# Snapshot AWS - Move and Copy!

This scripts export snapshots from one AWS Account to another and copy from one region to another! 

## Getting Started

### Prerequisites

- python 3
- boto3
- pip

### Installing

Clone this repository:

``` bash
git clone https://github.com/mandalvesq/snapshots-aws.git
```

Set the environment variables that refers to the AWS accounts.

```bash

export account_source=""
export account_destination=""
export bucket=""

```

And then run the scripts. 

First, to share the snapshots between accounts, run: 

```python3.7 scripts/snaps.py```

The output will be available in the AWS S3 Bucket provided in the environment variables in the path: 's3-bucket/history/snaps.json' 

Second, to migrate the snapshots between regions, run: 

```bash

export region_source=""
export region_destination=""

```

And then: 

```python3.7 scripts/copy-snaps.py```

