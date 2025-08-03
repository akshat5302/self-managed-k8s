import pulumi
from config import InfrastructureConfig
from vpc.vpc import VPCInfrastructure
from compute.ec2 import EC2Infrastructure

def main():
    # Initialize configuration
    config = InfrastructureConfig()
    
    # Create VPC infrastructure
    vpc_infra = VPCInfrastructure(
        name=config.vpc_name,
        cidr_block=config.vpc_cidr,
        availability_zones=config.availability_zones,
        public_subnet_cidrs=config.public_subnet_cidrs,
        private_subnet_cidrs=config.private_subnet_cidrs
    )
    
    # Create EC2 instances in private subnets
    ec2_infra = EC2Infrastructure(
        name=config.vpc_name,
        vpc_id=vpc_infra.vpc.id,
        private_subnet_ids=[subnet.id for subnet in vpc_infra.private_subnets],
        key_name=config.key_name,  # Optional: SSH key name
        instance_type_1=config.instance_type_1,  # 2 vCPU, 4GB RAM
        instance_type_2=config.instance_type_2    # 2 vCPU, 2GB RAM
    )
    
    # Export VPC outputs
    pulumi.export("vpc_id", vpc_infra.vpc.id)
    pulumi.export("vpc_cidr", vpc_infra.vpc.cidr_block)
    pulumi.export("internet_gateway_id", vpc_infra.internet_gateway.id)
    pulumi.export("nat_gateway_id", vpc_infra.nat_gateway.id)
    pulumi.export("nat_eip", vpc_infra.nat_eip.public_ip)
    
    # Export subnet information
    pulumi.export("public_subnet_ids", [subnet.id for subnet in vpc_infra.public_subnets])
    pulumi.export("private_subnet_ids", [subnet.id for subnet in vpc_infra.private_subnets])
    
    # Export route table information
    pulumi.export("public_route_table_id", vpc_infra.public_route_table.id)
    pulumi.export("private_route_table_id", vpc_infra.private_route_table.id)
    
    # Export EC2 information
    pulumi.export("master_security_group_id", ec2_infra.master_security_group.id)
    pulumi.export("worker_security_group_id", ec2_infra.worker_security_group.id)
    pulumi.export("master_instance_ids", [instance.id for instance in ec2_infra.master_instances])
    pulumi.export("worker_instance_ids", [instance.id for instance in ec2_infra.worker_instances])
    pulumi.export("all_instance_ids", [instance.id for instance in ec2_infra.instances])
    pulumi.export("master_instance_private_ips", [instance.private_ip for instance in ec2_infra.master_instances])
    pulumi.export("worker_instance_private_ips", [instance.private_ip for instance in ec2_infra.worker_instances])
    pulumi.export("all_instance_private_ips", [instance.private_ip for instance in ec2_infra.instances])

if __name__ == "__main__":
    main() 