import pulumi
import pulumi_aws as aws
import json

# Configuration
config = pulumi.Config()
bucket_name = config.get("bucket_name") or "my-self-managed-k8s-bucket"
region = config.get("region") or "us-west-1"

# Create S3 bucket
s3_bucket = aws.s3.Bucket("k8s-bucket",
    bucket=bucket_name,
    acl="private",
    versioning=aws.s3.BucketVersioningArgs(
        enabled=True
    ),
    tags={
        "Name": bucket_name,
        "Environment": "production",
        "Purpose": "kubernetes-storage"
    }
)

# Enable server-side encryption
encryption_configuration = aws.s3.BucketServerSideEncryptionConfiguration("k8s-bucket-encryption",
    bucket=s3_bucket.id,
    rules=[{
        "applyServerSideEncryptionByDefault": {
            "sseAlgorithm": "AES256"
        }
    }]
)

# Create bucket policy for additional security
bucket_policy = aws.s3.BucketPolicy("k8s-bucket-policy",
    bucket=s3_bucket.id,
    policy=pulumi.Output.all(s3_bucket.arn).apply(lambda args: json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DenyUnencryptedObjectUploads",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:PutObject",
                "Resource": f"{args[0]}/*",
                "Condition": {
                    "StringNotEquals": {
                        "s3:x-amz-server-side-encryption": "AES256"
                    }
                }
            },
            {
                "Sid": "DenyIncorrectEncryptionHeader",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:PutObject",
                "Resource": f"{args[0]}/*",
                "Condition": {
                    "StringNotEquals": {
                        "s3:x-amz-server-side-encryption": "AES256"
                    }
                }
            }
        ]
    }))
)

# Outputs
pulumi.export("bucket_name", s3_bucket.bucket)
pulumi.export("bucket_arn", s3_bucket.arn)
pulumi.export("bucket_region", s3_bucket.region)
pulumi.export("bucket_domain_name", s3_bucket.bucket_domain_name) 