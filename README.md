# self-managed-k8s
A Self Managed kubernetes on ec2 instances nodes

## S3 Bucket Setup

This Pulumi project creates a secure S3 bucket for storing Kubernetes-related data and backups.

### Features

- **Encrypted Storage**: Server-side encryption with AES256
- **Versioning**: Enabled for data protection and recovery
- **Security Policy**: Denies unencrypted uploads
- **Private Access**: Bucket is private by default

### Prerequisites

- Python 3.7+
- Pulumi CLI
- AWS CLI configured with appropriate credentials

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your AWS credentials:
```bash
aws configure
```

### Usage

1. Select a stack:
```bash
# For development
pulumi stack select dev

# For production
pulumi stack select prod
```

2. Preview changes:
```bash
pulumi preview
```

3. Deploy:
```bash
pulumi up
```

4. View outputs:
```bash
pulumi stack output
```

### Configuration

You can customize the bucket settings by modifying the stack configuration files:
- `Pulumi.dev.yaml` - Development environment settings
- `Pulumi.prod.yaml` - Production environment settings

### Outputs

After deployment, you'll get:
- `bucket_name`: The name of the created S3 bucket
- `bucket_arn`: The ARN of the bucket
- `bucket_region`: The region where the bucket is located
- `bucket_domain_name`: The domain name for the bucket
