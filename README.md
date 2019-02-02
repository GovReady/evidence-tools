# evidence-uploader

Uploads an evidence file to an S3 bucket.

Currently broken, returns `403 Forbidden`. Cause under investigation.

Overview:

* Set up S3 bucket, bucket policy, and IAM user.  See example policy, apply it to a user.
* Run with `./eu.py -f extras/sample-image/image.png`
