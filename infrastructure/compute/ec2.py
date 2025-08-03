import pulumi
import pulumi_aws as aws

class EC2Infrastructure:
    def __init__(self, name: str, vpc_id: str, private_subnet_ids: list, 
                 key_name: str = None, instance_type_1: str = "c7gn.large", 
                 instance_type_2: str = "c7gn.medium"):
        self.name = name
        self.vpc_id = vpc_id
        self.private_subnet_ids = private_subnet_ids
        self.key_name = key_name
        self.instance_type_1 = "c7gn.large"  # 2 vCPU, 4GB RAM
        self.instance_type_2 = "c6g.medium"  # 2 vCPU, 2GB RAM
        
        # Create security group for EC2 instances
        self.master_security_group = aws.ec2.SecurityGroup(f"{name}-master-sg",
            description="Security group for EC2 instances in private subnets",
            vpc_id=vpc_id,
            ingress=[],
            egress=[
                aws.ec2.SecurityGroupEgressArgs(
                    description="All outbound traffic",
                    from_port=0,
                    to_port=0,
                    protocol="-1",
                    cidr_blocks=["0.0.0.0/0"]
                )
            ],
            tags={
                "Name": f"{name}-master-sg",
                "Environment": "dev",
                "Purpose": "kubernetes-master-nodes"
            }
        )

        self.worker_security_group = aws.ec2.SecurityGroup(f"{name}-worker-sg",
            description="Security group for EC2 instances in private subnets",
            vpc_id=vpc_id,
            ingress=[],
            egress=[
                aws.ec2.SecurityGroupEgressArgs(
                    description="All outbound traffic",
                    from_port=0,
                    to_port=0,
                    protocol="-1",
                    cidr_blocks=["0.0.0.0/0"]
                )
            ],
            tags={
                "Name": f"{name}-worker-sg",
                "Environment": "dev",
                "Purpose": "kubernetes-worker-nodes"
            }
        )
        
        # Create EC2 instances
        self.master_instances = []
        self.worker_instances = []
        
        # Create 1 master instance with 2 vCPU and 4GB RAM (t3.medium)
        for i in range(1):
            subnet_id = private_subnet_ids[i % len(private_subnet_ids)]
            instance = aws.ec2.Instance(f"{name}-master-{i+1}",
                ami="ami-001991993fd5323ab",  # Amazon Linux 2023 AMI
                instance_type=self.instance_type_1,
                subnet_id=subnet_id,
                vpc_security_group_ids=[self.master_security_group.id],
                key_name=key_name,
                associate_public_ip_address=False,  # Private subnet
                root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
                    volume_size=50,
                    volume_type="gp3",
                    delete_on_termination=True
                ),
                # user_data=self._get_user_data(),
                tags={
                    "Name": f"{name}-master-{i+1}",
                    "Environment": "dev",
                    "Purpose": "kubernetes-node",
                    "Type": "master"
                }
            )
            self.master_instances.append(instance)
        
        # Create 2 worker instances with 2 vCPU and 2GB RAM (t3.small)
        for i in range(2):
            subnet_id = private_subnet_ids[(i + 1) % len(private_subnet_ids)]
            instance = aws.ec2.Instance(f"{name}-worker-{i+1}",
                ami="ami-001991993fd5323ab",  # Amazon Linux 2023 AMI
                instance_type=self.instance_type_2,
                subnet_id=subnet_id,
                vpc_security_group_ids=[self.worker_security_group.id],
                key_name=key_name,
                associate_public_ip_address=False,  # Private subnet
                root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
                    volume_size=50,
                    volume_type="gp3",
                    delete_on_termination=True
                ),
                # user_data=self._get_user_data(),
                tags={
                    "Name": f"{name}-worker-{i+1}",
                    "Environment": "dev",
                    "Purpose": "kubernetes-node",
                    "Type": "worker"
                }
            )
            self.worker_instances.append(instance)
        
        # Combine all instances for easy access
        self.instances = self.master_instances + self.worker_instances

#     def _get_user_data(self):
#         """Return user data script for EC2 instances (Amazon Linux 2023)"""
#         return """#!/bin/bash
# # Update system
# # dnf update -y

# # # Install Docker
# # dnf install -y docker
# # systemctl start docker
# # systemctl enable docker

# # # Install additional tools
# # dnf install -y curl wget git

# # # Configure Docker to use systemd
# # mkdir -p /etc/docker
# # cat > /etc/docker/daemon.json <<EOF
# # {
# #   "exec-opts": ["native.cgroupdriver=systemd"],
# #   "log-driver": "json-file",
# #   "log-opts": {
# #     "max-size": "100m"
# #   },
# #   "storage-driver": "overlay2"
# # }
# # EOF

# # systemctl daemon-reload
# # systemctl restart docker

# # # Install Kubernetes components
# # cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
# # [kubernetes]
# # name=Kubernetes
# # baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el9-x86_64
# # enabled=1
# # gpgcheck=1
# # repo_gpgcheck=1
# # gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
# # exclude=kubelet kubeadm kubectl
# # EOF

# # # Install kubelet, kubeadm, and kubectl
# # dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
# # systemctl enable kubelet
# # systemctl start kubelet

# # # Disable swap
# # swapoff -a
# # sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# # # Load kernel modules
# # cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
# # overlay
# # br_netfilter
# # EOF

# # modprobe overlay
# # modprobe br_netfilter

# # # Set kernel parameters
# # cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
# # net.bridge.bridge-nf-call-iptables  = 1
# # net.bridge.bridge-nf-call-ip6tables = 1
# # net.ipv4.ip_forward                 = 1
# # EOF

# # sysctl --system

# # echo "EC2 instance setup completed!"
# # """ 