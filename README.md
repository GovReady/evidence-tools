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
* Edit `eu.py` to include access key ID and secret access key of user.

### Run Script

* `./eu.py -f extras/sample-image/image.png`
