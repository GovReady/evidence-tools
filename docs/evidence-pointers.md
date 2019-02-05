# Evidence pointer brainstorming

(evidence server : system name : evidence)
evidence-server-001 : cace-austin : aws-mfa-scrn/
evidence-server-001 : cace-los-angeles : aws-mfa-scrn/
evidence-server-021 : cbp-website-prod : aws-mfa-scrn/
evidence-server-021 : cbp-website-staging : aws-mfa-scrn/

"evidence-server" is really an S3 endpoint, like
`https://s3-us-west-2.amazonaws.com` + a bucket name, like
`govready-evidence-qb9zxvylp8dluv5bcg1exb`.  Multiple evidence servers
are specified in the evidence server search path.
