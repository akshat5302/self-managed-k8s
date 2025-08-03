# self-managed-k8s
A Self Managed Kubernetes cluster on EC2 instances with proper VPC infrastructure

## Infrastructure Setup

This Pulumi project creates a complete infrastructure for hosting a self-managed Kubernetes cluster.

### Features

- **VPC**: Custom VPC with DNS support enabled
- **Subnets**: 2 public and 2 private subnets across 2 availability zones
- **Internet Gateway**: For public internet access
- **NAT Gateway**: For private subnet internet access
- **Route Tables**: Properly configured routing for public and private subnets
- **EC2 Instances**: 3 Kubernetes nodes in private subnets
  - 1 master node with 2 vCPU and 4GB RAM (t3.medium)
  - 2 worker nodes with 2 vCPU and 2GB RAM (t3.small)
- **Security Groups**: Empty security groups for master nodes, configured security group for worker nodes
- **High Availability**: Multi-AZ deployment for reliability

### Infrastructure Components

- **VPC**: 10.0.0.0/16 CIDR block
- **Public Subnets**: 
  - us-east-1a: 10.0.1.0/24
  - us-east-1b: 10.0.2.0/24
- **Private Subnets**:
  - us-east-1a: 10.0.11.0/24
  - us-east-1b: 10.0.12.0/24
- **Internet Gateway**: For public subnets
- **NAT Gateway**: For private subnets (placed in first public subnet)
- **Route Tables**: Separate routing for public and private subnets
- **EC2 Instances**: 3 nodes distributed across private subnets
- **Security Groups**: 
  - Empty Security Group: No inbound rules, outbound traffic allowed
  - Master Security Group: No inbound rules, outbound traffic allowed
  - Worker Security Group: HTTP, HTTPS, NodePort services, Kubelet API

### Prerequisites

- Python 3.7+
- Pulumi CLI
- AWS CLI configured with appropriate credentials

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

You can customize the infrastructure settings by modifying the stack configuration files:
- `Pulumi.dev.yaml` - Development environment settings
- `Pulumi.prod.yaml` - Production environment settings

### Outputs

After deployment, you'll get:
- `vpc_id`: The ID of the created VPC
- `vpc_cidr`: The CIDR block of the VPC
- `internet_gateway_id`: The ID of the Internet Gateway
- `nat_gateway_id`: The ID of the NAT Gateway
- `nat_eip`: The Elastic IP address of the NAT Gateway
- `public_subnet_ids`: List of public subnet IDs
- `private_subnet_ids`: List of private subnet IDs
- `public_route_table_id`: The ID of the public route table
- `private_route_table_id`: The ID of the private route table
- `empty_security_group_id`: The ID of the empty security group
- `master_security_group_id`: The ID of the master security group
- `worker_security_group_id`: The ID of the worker security group
- `master_instance_ids`: List of master instance IDs
- `worker_instance_ids`: List of worker instance IDs
- `all_instance_ids`: List of all instance IDs
- `master_instance_private_ips`: List of master instance private IPs
- `worker_instance_private_ips`: List of worker instance private IPs
- `all_instance_private_ips`: List of all instance private IPs

### Project Structure

```
self-managed-k8s/
├── infrastructure/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── vpc/
│   │   ├── __init__.py
│   │   └── vpc.py
│   ├── compute/
│   │   ├── __init__.py
│   │   └── ec2.py
│   ├── networking/
│   └── security/
├── __main__.py
├── Pulumi.yaml
├── Pulumi.dev.yaml
├── Pulumi.prod.yaml
├── requirements.txt
└── README.md
```

### EC2 Instance Specifications

- **1 Master Node** (t3.medium):
  - 2 vCPU
  - 4GB RAM
  - 50GB GP3 storage
  - Amazon Linux 2023 AMI
  - Empty Master Security Group

- **2 Worker Nodes** (t3.small):
  - 2 vCPU
  - 2GB RAM
  - 50GB GP3 storage
  - Amazon Linux 2023 AMI
  - Worker Security Group

### Security Groups

#### Empty Security Group
- **No inbound rules**: Completely closed for incoming traffic
- **All outbound traffic**: Allows all outbound traffic
- **Purpose**: For resources that need no inbound access

#### Master Security Group
- **No inbound rules**: Completely closed for incoming traffic
- **All outbound traffic**: Allows all outbound traffic
- **Purpose**: For master nodes that don't need direct inbound access

#### Worker Security Group
- **SSH** (22): Access from anywhere
- **HTTP** (80): Web traffic
- **HTTPS** (443): Secure web traffic
- **Kubelet API** (10250): Kubelet communication
- **NodePort Services** (30000-32767): Kubernetes NodePort services
- **Internal traffic**: All traffic within the security group

### S3 Backend
`pulumi config set aws:region us-east-1`
`pulumi login s3://pulumi-remote-state-backend`
