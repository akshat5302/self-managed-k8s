import pulumi
import pulumi_aws as aws

class VPCInfrastructure:
    def __init__(self, name: str, cidr_block: str, availability_zones: list, 
                 public_subnet_cidrs: list, private_subnet_cidrs: list):
        self.name = name
        self.cidr_block = cidr_block
        self.availability_zones = availability_zones
        self.public_subnet_cidrs = public_subnet_cidrs
        self.private_subnet_cidrs = private_subnet_cidrs
        
        # Create VPC
        self.vpc = aws.ec2.Vpc(f"{name}-vpc",
            cidr_block=cidr_block,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags={
                "Name": f"{name}-vpc",
                "Environment": "dev",
                "Purpose": "kubernetes-cluster"
            }
        )
        
        # Create Internet Gateway
        self.internet_gateway = aws.ec2.InternetGateway(f"{name}-igw",
            vpc_id=self.vpc.id,
            tags={
                "Name": f"{name}-igw",
                "Environment": "dev"
            }
        )
        
        # Create public subnets
        self.public_subnets = []
        for i, (az, cidr) in enumerate(zip(availability_zones, public_subnet_cidrs)):
            subnet = aws.ec2.Subnet(f"{name}-public-subnet-{i+1}",
                vpc_id=self.vpc.id,
                cidr_block=cidr,
                availability_zone=az,
                map_public_ip_on_launch=True,
                tags={
                    "Name": f"{name}-public-subnet-{i+1}",
                    "Environment": "dev",
                    "Type": "public"
                }
            )
            self.public_subnets.append(subnet)
        
        # Create private subnets
        self.private_subnets = []
        for i, (az, cidr) in enumerate(zip(availability_zones, private_subnet_cidrs)):
            subnet = aws.ec2.Subnet(f"{name}-private-subnet-{i+1}",
                vpc_id=self.vpc.id,
                cidr_block=cidr,
                availability_zone=az,
                map_public_ip_on_launch=False,
                tags={
                    "Name": f"{name}-private-subnet-{i+1}",
                    "Environment": "dev",
                    "Type": "private"
                }
            )
            self.private_subnets.append(subnet)
        
        # Create Elastic IP for NAT Gateway
        self.nat_eip = aws.ec2.Eip(f"{name}-nat-eip",
            domain="vpc",
            tags={
                "Name": f"{name}-nat-eip",
                "Environment": "dev"
            }
        )
        
        # Create NAT Gateway
        self.nat_gateway = aws.ec2.NatGateway(f"{name}-nat",
            allocation_id=self.nat_eip.id,
            subnet_id=self.public_subnets[0].id,  # Place in first public subnet
            tags={
                "Name": f"{name}-nat",
                "Environment": "dev"
            }
        )
        
        # Create route tables
        self._create_route_tables()
    
    def _create_route_tables(self):
        # Public route table
        self.public_route_table = aws.ec2.RouteTable(f"{self.name}-public-rt",
            vpc_id=self.vpc.id,
            routes=[
                aws.ec2.RouteTableRouteArgs(
                    cidr_block="0.0.0.0/0",
                    gateway_id=self.internet_gateway.id
                )
            ],
            tags={
                "Name": f"{self.name}-public-rt",
                "Environment": "dev"
            }
        )
        
        # Private route table
        self.private_route_table = aws.ec2.RouteTable(f"{self.name}-private-rt",
            vpc_id=self.vpc.id,
            routes=[
                aws.ec2.RouteTableRouteArgs(
                    cidr_block="0.0.0.0/0",
                    nat_gateway_id=self.nat_gateway.id
                )
            ],
            tags={
                "Name": f"{self.name}-private-rt",
                "Environment": "dev"
            }
        )
        
        # Associate public subnets with public route table
        self.public_route_table_associations = []
        for i, subnet in enumerate(self.public_subnets):
            association = aws.ec2.RouteTableAssociation(f"{self.name}-public-rta-{i+1}",
                subnet_id=subnet.id,
                route_table_id=self.public_route_table.id
            )
            self.public_route_table_associations.append(association)
        
        # Associate private subnets with private route table
        self.private_route_table_associations = []
        for i, subnet in enumerate(self.private_subnets):
            association = aws.ec2.RouteTableAssociation(f"{self.name}-private-rta-{i+1}",
                subnet_id=subnet.id,
                route_table_id=self.private_route_table.id
            )
            self.private_route_table_associations.append(association) 