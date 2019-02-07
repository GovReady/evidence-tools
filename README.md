# evidence-uploader

Uploads an evidence file to an S3 bucket.

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
* `./eu.py -b govready-es-srv-01 -f extras/sample-image/image.png`

### Specify Metadata

Use `-m KEY=VALUE` or `--metadata KEY=VALUE` to specify metadata. Multiple flags are allowed.  If a KEY or VALUE contains space characters, use quotes around the string.  Note that user-defined metadata is limited to 2KB in PUT requests.  See [Object Key and Metadata](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html) in the AWS docs for more details.

Example:
* `./eu.py -m a=b -m c="dogs and cats" -b govready-es-srv-01 -f extras/sample-image/image.png`

### Strip Dirpath

Without `--strip`, any directory path to the uploaded file is removed.  If `--strip DIRPATH` is included, only the specified DIRPATH is removed from the uploaded filename.

For example, the following command without `--strip` names the uploaded file "image.png":

* `./eu.py -b govready-es-srv-01 -f extras/sample-image/image.png`

The following command with `--strip` names the uploaded file "sample-image/image.png":

* `./eu.py -b govready-es-srv-01 --strip extras/ -f extras/sample-image/image.png`

### Example: `find` and `--strip`

Assume a directory structure like this:

* path
  * to
    * my
      * evidence folders
        * AC
        * AT
        * AU
        * CM
        * ... etc.


This command will find all files (using `-type f`) in `evidence folders`, and strip everything from the dirpath except `AC/`, `AT/`, 'AU/`, `CM/`, etc.

* `find "/path/to/my/evidence folders" -type f -exec ./eu.py -m org=MyOrg -m system=MySystem -b MyOrg-MySystem-es-srv1 --strip "/path/to/my/evidence folders/" -f "{}" \;`

By adding an extra `-exec echo "{}"` clause, a simple progress monitor will added, which prints the full filepath for each file uploaded.

* `find "/path/to/my/evidence folders" -type f -exec ./eu.py -m org=MyOrg -m system=MySystem -b MyOrg-MySystem-es-srv1 --strip "/path/to/my/evidence folders/" -f "{}" \; -exec echo "{}" \;`