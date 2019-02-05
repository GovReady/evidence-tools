# evidence-uploader

Uploads an evidence file to an S3 bucket.

Currently broken, returns `403 Forbidden`. Cause under investigation.

### Script Setup

* clone repo, cd to its directory
* `virtualenv venv -p python3`
* `pip install -r requirements.txt`
* `source venv/bin/activate`

### AWS Setup

* Set up S3 bucket, bucket policy, and IAM user.  See [example policy](extras/sample-s3-policy.json), apply it to a user.
* Copy `env.sh-template` to `env.sh` and edit to include access key ID and secret access key of user.

### Run Script

* `source env.sh`
* `./eu.py -b govready-evidence-qb9zxvylp8dluv5bcg1exb -f extras/sample-image/image.png`

### Specify Metadata

Use `-m KEY=VALUE` or `--metadata KEY=VALUE` to specify metadata. Multiple flags are allowed.  If a KEY or VALUE contains space characters, use quotes around the string.  Note that user-defined metadata is limited to 2KB in PUT requests.  See [Object Key and Metadata](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html) in the AWS docs for more details.

Example:
* `./eu.py -m a=b -m c="dogs and cats" -b govready-evidence-qb9zxvylp8dluv5bcg1exb -f extras/sample-image/image.png`
