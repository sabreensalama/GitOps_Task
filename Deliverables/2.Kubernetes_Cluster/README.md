# Install Multipass on macOS
brew install --cask multipass

# Create the Kubernetes VMs
multipass launch 22.04 --name master --cpus 2 --memory 4G --disk 20G
multipass launch 22.04 --name worker1 --cpus 2 --memory 4G --disk 20G

# Verify the VMs
multipass list

################################################################################
# MASTER NODE
################################################################################

multipass shell master

# Install containerd
sudo apt update
sudo apt install -y containerd

sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# Configure containerd to use systemd cgroups
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' \
/etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd

# Configure required kernel modules
sudo modprobe overlay
sudo modprobe br_netfilter
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

# Configure Kubernetes networking
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables=1
net.bridge.bridge-nf-call-ip6tables=1
net.ipv4.ip_forward=1
EOF
sudo sysctl --system

# Install Kubernetes packages
sudo apt install -y apt-transport-https ca-certificates curl

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.35/deb/Release.key | \
sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.35/deb/ /" | \
sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Initialize the cluster
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Configure kubectl for the ubuntu user
mkdir -p $HOME/.kube
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Install Flannel CNI
kubectl apply -f \
https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml

################################################################################
# WORKER NODE
################################################################################

multipass shell worker1

# Install containerd
sudo apt update
sudo apt install -y containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' \
/etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd

# Configure required kernel modules
sudo modprobe overlay
sudo modprobe br_netfilter
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables=1
net.bridge.bridge-nf-call-ip6tables=1
net.ipv4.ip_forward=1
EOF
sudo sysctl --system

# Install Kubernetes packages
sudo apt install -y apt-transport-https ca-certificates curl

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.35/deb/Release.key | \
sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.35/deb/ /" | \
sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install -y kubelet kubeadm
sudo apt-mark hold kubelet kubeadm

# Join the cluster
sudo kubeadm join 192.168.252.4:6443 --token knxz30.gjzql1b8pi565g1t \
	--discovery-token-ca-cert-hash sha256:0b741fdd8371f8e1a01b1d6901a5fd9b1508523bc41d6c925b529153274d6b40 

################################################################################
# CONFIGURE kubectl ON THE MAC
################################################################################

mkdir -p ~/.kube

multipass exec master -- \
sudo cat /etc/kubernetes/admin.conf > ~/.kube/config

# Verify the cluster
kubectl get nodes

################################################################################
# OPTIONAL - Restrict Kubernetes API Access
################################################################################

# Install and configure UFW on the master.

sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow 22/tcp
sudo ufw allow from <TRUSTED_IP_OR_SUBNET> to any port 6443 proto tcp

sudo ufw enable

################################################################################
# INSTALL NGINX INGRESS
################################################################################

kubectl apply -f \
https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# Required for local Multipass environments so NodePort traffic
# is forwarded to the node hosting the ingress controller.

kubectl patch svc ingress-nginx-controller \
  -n ingress-nginx \
  -p '{"spec":{"externalTrafficPolicy":"Cluster"}}'

################################################################################
# DEPLOY JUICE SHOP
################################################################################

kubectl apply -f kubernetes-cluster/juice-shop.yaml

##### Monitoring Stack
I would recommend a standard Kubernetes monitoring stack like this:


Prometheus	Collect metrics from Kubernetes and Juice Shop
Alertmanager	Send alerts when thresholds are exceeded
Grafana	Dashboards and visualization
kube-state-metrics	Kubernetes object metrics
Node Exporter	Node CPU, memory, disk metrics
cAdvisor	Container CPU, memory, filesystem metrics
Loki	Centralized application logs
Promtail	Collect logs from pods and send them to Loki
