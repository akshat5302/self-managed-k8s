import pulumi

class InfrastructureConfig:
    def __init__(self):
        config = pulumi.Config()
        
        # VPC Configuration
        self.vpc_name = config.get("vpc_name") or "k8s-cluster"
        self.vpc_cidr = config.get("vpc_cidr") or "10.0.0.0/16"
        self.region = config.get("aws:region") or "us-east-1"
        
        # Availability Zones (default to us-east-1)
        self.availability_zones = [
            f"{self.region}a",
            f"{self.region}b"
        ]
        
        # Subnet CIDR blocks - read from individual config keys
        self.public_subnet_cidrs = [
            config.get("public_subnet_1_cidr") or "10.0.1.0/24",
            config.get("public_subnet_2_cidr") or "10.0.2.0/24"
        ]
        
        self.private_subnet_cidrs = [
            config.get("private_subnet_1_cidr") or "10.0.11.0/24",
            config.get("private_subnet_2_cidr") or "10.0.12.0/24"
        ]
        
        # EC2 Configuration
        self.key_name = config.get("key_name")  # Optional SSH key name
        self.instance_type_1 = config.get("instance_type_1") or "t3.medium"  # 2 vCPU, 4GB RAM
        self.instance_type_2 = config.get("instance_type_2") or "t3.small"    # 2 vCPU, 2GB RAM
        
        # Tags
        self.common_tags = {
            "Environment": "dev",
            "Project": "self-managed-k8s",
            "ManagedBy": "pulumi"
        } 