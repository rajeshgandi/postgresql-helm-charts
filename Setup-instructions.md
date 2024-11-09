# PostgreSQL Cluster with Load Balancer and Replication on Minikube

**Overview**

This project demonstrates the deployment and management of a PostgreSQL database cluster with a load balancer using Kubernetes and Helm. It also showcases asynchronous replication to a standalone PostgreSQL database.

### Requirement

1. Using Minikube, deploy a small Kubernetes cluster in your local environment. This won’t require a lot of resources, 2 CPU 2 GB RAM and 20GB disk space will do. 
2. Using Helm Chart, deploy a PostgreSQL database cluster with a load balancer. 
3. You are not limited to the number of nodes in the cluster, decide on the number based on your machine’s resource availability. 
4. You are not limited to the specs for the nodes e.g mem, storage, vCPU. Decide on the number based on your machine’s resource availability. 
5. Develop a script/code to create a simple database with two related tables using a foreign key. 
6. Using the Faker library, or any other random data generation library you are familiar with, insert 100,000 records into the two tables. 
7. Using Helm Chart still, deploy a standalone PostgreSQL database, then setup an async replication from your cluster to this standalone database. 
8. Push your codes to Github.

### Expected deliverables

1. An architectural diagram showing your solution architecture, together with documentation. 
2. A Git repo containing Helm Charts and codes/scripts to deploy a PostgreSQL database cluster with a load balancer, and schema/tables/records. Senior Database Administrator Assignment 1 
3. PostgreSQL database cluster with a load balancer, and schema/tables/records. 
4. The standalone replica database needs to be in sync with the main cluster showing the replicated records. 

## Setup requirements

-  CentOS 9: Virtual Machine for Minikube setup.
-  Minikube: A small Kubernetes cluster deployed on your local machine (2 CPUs, 2GB RAM, and 20GB disk). -
-  Helm: A package manager for Kubernetes, used to deploy and manage PostgreSQL deployments.
-  ython: For running a data insertion script that populates PostgreSQL tables with 100,000 records using the Faker library.

## Setup instructions and sample outputs

The following set up is ran on Cent OS 9 Virtual machine.

## Table of Contents
- [Pre-requisites](#Pre-requisites)
  - [Install PostgreSQL Client on VM](#1-install-postgresql-client-on-vm)
  - [Install and docker](#2-install-and-docker)
  - [Install Python to load the data](#3-install-python-to-load-the-data)
  - [Install and Start Minikube](#4-install-and-start-minikube)
  - [Install kubectl](#5-install-kubectl)
  - [Install and Configure Helm](#6-install-and-configure-helm)
  - [Download the helm charts to deploy PostgreSQL](#7-download-the-helm-charts-to-deploy-postgresql)
  - [PostgreSQL Deployment](#postgresql-deployment)
- [PostgreSQL Deployment](#postgresql-deployment)
  - [Deploy PostgreSQL Database Cluster with Helm](#1-deploy-postgresql-database-cluster-with-helm)
  - [Login to the pod and create required tables and install vi and procps](#2-login-to-the-pod-and-create-required-tables-and-install-vi-and-procps)
  - [Stay within the pod and create tables](#3-stay-within-the-pod-and-create-tables)
  - [From the VM, insert the data.](#4-from-the-vm-insert-the-data)
- [Set up replication for primary deployment](#set-up-replication-for-primary-deployment)
- [Set up standalone PostgreSQL deployment and convert it as replica for current primary](#set-up-standalone-postgresql-deployment-and-convert-it-as-replica-for-current-primary)
- [Convert the standalone-postgresql-548f49dc97-spkjs to replica](#convert-the-standalone-postgresql-548f49dc97-spkjs-to-replica)
- [Push the code to git](#to-push-your-folder-to-git-follow-these-steps)
  
## Pre-requisites

### 1. Install PostgreSQL Client on VM

```
dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm
dnf -qy module disable postgresql
dnf install -y postgresql17-server
```
### 2. Install and docker

```
dnf install -y dnf-plugins-core
dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
dnf install -y docker-ce docker-ce-cli containerd.io
systemctl enable --now docker
systemctl start docker
```

After successful installation, docker status should look like below

```
[root@lab01 ~]# systemctl status docker
● docker.service - Docker Application Container Engine
     Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; preset: disabled)
     Active: active (running) since Sat 2024-11-09 01:05:43 IST; 6s ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 37006 (dockerd)
      Tasks: 9
     Memory: 23.6M
        CPU: 156ms
     CGroup: /system.slice/docker.service
             └─37006 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

Nov 09 01:05:41 lab01 dockerd[37006]: time="2024-11-09T01:05:41.566266827+05:30" level=info msg="Loading containers: start."
Nov 09 01:05:41 lab01 dockerd[37006]: time="2024-11-09T01:05:41.595896119+05:30" level=info msg="Firewalld: created docker-forwarding >
Nov 09 01:05:42 lab01 dockerd[37006]: time="2024-11-09T01:05:42.916140107+05:30" level=info msg="Firewalld: interface docker0 already >
Nov 09 01:05:43 lab01 dockerd[37006]: time="2024-11-09T01:05:43.107691425+05:30" level=info msg="Loading containers: done."
```
### 3. Install Python to load the data

```
sudo dnf install -y python3
dnf install python3-pip -y
pip3 install faker psycopg2-binary
```

### 4. Install and Start Minikube

```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start --driver=docker --cpus=2 --memory=2048mb --disk-size=20g --force
```
To check if it has successfully configured run `minikube status` and you get something like below

```
[root@lab01 ~]# minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

### 5. Install kubectl

```
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

Verify the installation

```
[root@lab01 ~]# kubectl version --client
Client Version: v1.31.0
Kustomize Version: v5.4.2
[root@lab01 ~]#
```

### 6. Install and Configure Helm

```
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

Output for the last command should be something like

```
[root@lab01 ~]# helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈Happy Helming!⎈
[root@lab01 ~]#
```

### 7. Download the helm charts to deploy PostgreSQL

```
sudo dnf install -y git
git clone https://github.com/postgrestraining/postgresql-helm-charts.git
cd postgresql-helm-charts
```

## PostgreSQL Deployment

### 1. Deploy PostgreSQL Database Cluster with Helm

```
cd /root/postgresql-helm-charts
helm install primary-postgresql ./chart-primary
```

Check if the deployment is configured with LoadBalancer

```
[root@lab01 postgresql-helm-charts]# kubectl describe svc primary-postgresql | grep Type
Type:                     LoadBalancer
[root@lab01 postgresql-helm-charts]#
```

Check if the deployment is successful, the output should look like this 

```
[root@lab01 postgresql-helm-charts]# helm install primary-postgresql ./chart-primary
NAME: primary-postgresql
LAST DEPLOYED: Sat Nov  9 01:23:46 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None

[root@lab01 postgresql-helm-charts]# kubectl get pods
NAME                                 READY   STATUS    RESTARTS   AGE
primary-postgresql-66bd47f89-jnpnj   1/1     Running   0          42s

[root@lab01 postgresql-helm-charts]# kubectl get svc
NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes           ClusterIP      10.96.0.1       <none>        443/TCP          13m
primary-postgresql   LoadBalancer   10.105.10.137   <pending>     5432:30467/TCP   45s
[root@lab01 postgresql-helm-charts]#
```

### 2. Login to the pod and create required tables and install vi and procps 

**Command to login:** `kubectl exec -it <pod_name derived from kubectl get pods> -- /bin/bash`

```
kubectl exec -it primary-postgresql-66bd47f89-jnpnj -- /bin/bash
apt-get update
apt install vi
apt install procps
```

**exit and login as postgres user:** `kubectl exec -it <pod_name derived from kubectl get pods> -- su - postgres`

```
[root@lab01 postgresql-helm-charts]# kubectl exec -it primary-postgresql-66bd47f89-jnpnj -- su - postgres
postgres@primary-postgresql-66bd47f89-jnpnj:~$ cd /var/lib/postgresql/data
postgres@primary-postgresql-66bd47f89-jnpnj:~/data$ vi pg_hba.conf
..
host    replication     all             0.0.0.0/0               trust
host    all             all             0.0.0.0/0               trust
..
..

postgres@primary-postgresql-66bd47f89-jnpnj:~/data$ psql
psql (17.0 (Debian 17.0-1.pgdg120+1))
Type "help" for help.

postgres=# select pg_reload_conf();
 pg_reload_conf
----------------
 t
(1 row)

```
### 3. Stay within the pod and create tables

```
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_id INT REFERENCES authors(author_id)
);

CREATE TABLE test (
	id int,
	val int
);

insert into test values(1,1);
```
### 4. From the VM, insert the data. 

- Use port forwarding to to load the data from python script.

**Session 1**

```
[root@lab01 postgresql-helm-charts]# kubectl get svc
NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes           ClusterIP      10.96.0.1       <none>        443/TCP          31m
primary-postgresql   LoadBalancer   10.105.10.137   <pending>     5432:30467/TCP   18m
[root@lab01 postgresql-helm-charts]#

[root@lab01 postgresql-helm-charts]# kubectl port-forward svc/primary-postgresql 5432:5432
Forwarding from 127.0.0.1:5432 -> 5432
Forwarding from [::1]:5432 -> 5432

```

While the session in open state, open session 2

**Session 2**

```
cd /root/postgresql-helm-charts
python3.9 fake_inserts.py
```

Output should look like this

```
[root@lab01 postgresql-helm-charts]# python3.9 fake_inserts.py
Inserting authors...
Total authors inserted: 1000
Inserting books...
5000 books inserted...
10000 books inserted...
15000 books inserted...
20000 books inserted...
25000 books inserted...
30000 books inserted...
35000 books inserted...
40000 books inserted...
45000 books inserted...
50000 books inserted...
55000 books inserted...
60000 books inserted...
65000 books inserted...
70000 books inserted...
75000 books inserted...
80000 books inserted...
85000 books inserted...
90000 books inserted...
95000 books inserted...
100000 books inserted...
Total books inserted: 100000
Data insertion completed.
[root@lab01 postgresql-helm-charts]#

[root@lab01 postgresql-helm-charts]# kubectl exec -it primary-postgresql-66bd47f89-jnpnj -- su - postgres
postgres@primary-postgresql-66bd47f89-jnpnj:~$ psql
psql (17.0 (Debian 17.0-1.pgdg120+1))
Type "help" for help.

postgres=# \dt+
                                      List of relations
 Schema |  Name   | Type  |  Owner   | Persistence | Access method |    Size    | Description
--------+---------+-------+----------+-------------+---------------+------------+-------------
 public | authors | table | postgres | permanent   | heap          | 80 kB      |
 public | books   | table | postgres | permanent   | heap          | 7552 kB    |
 public | test    | table | postgres | permanent   | heap          | 8192 bytes |
(3 rows)

postgres=# select count(1) from books;
 count
--------
 100000
(1 row)

postgres=#
```

## Set up replication for primary deployment

```
cd /root/postgresql-helm-charts
helm install replica-postgresql ./chart-replica/
```

- Get the pod name and check if the data replicated

```
[root@lab01 postgresql-helm-charts]# kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
primary-postgresql-66bd47f89-jnpnj    1/1     Running   0          26m
replica-postgresql-6484bfbf6f-4nh6f   1/1     Running   0          6s
[root@lab01 postgresql-helm-charts]#

[root@lab01 postgresql-helm-charts]# kubectl exec -it replica-postgresql-6484bfbf6f-4nh6f -- psql -U postgres
Defaulted container "postgres" out of: postgres, pg-basebackup (init)
psql (17.0 (Debian 17.0-1.pgdg120+1))
Type "help" for help.

postgres=# psql
postgres=# select count(1) from books;
 count
--------
 100000
(1 row)

postgres=# delete from books;
ERROR:  cannot execute DELETE in a read-only transaction
postgres=#
```
## Set up standalone PostgreSQL deployment and convert it as replica for current primary

```
cd /root/postgresql-helm-charts
helm install standalone-postgresql ./chart-standalone/
```

- Since it is a standalone deployment, you can do read/write operation

```
[root@lab01 postgresql-helm-charts]# kubectl get pods
NAME                                     READY   STATUS    RESTARTS   AGE
primary-postgresql-66bd47f89-jnpnj       1/1     Running   0          31m
replica-postgresql-6484bfbf6f-4nh6f      1/1     Running   0          4m48s
standalone-postgresql-548f49dc97-spkjs   1/1     Running   0          5s

[root@lab01 postgresql-helm-charts]# kubectl exec -it standalone-postgresql-548f49dc97-spkjs -- psql -U postgres
psql (17.0 (Debian 17.0-1.pgdg120+1))
Type "help" for help.

postgres=#
postgres=# \dt+
Did not find any relations.
postgres=# create table emp(id int,sal int);
CREATE TABLE
postgres=#
```

## Convert the standalone-postgresql-548f49dc97-spkjs to replica

```
- Before that get svc details

[root@lab01 postgresql-helm-charts]# kubectl get svc
NAME                    TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes              ClusterIP      10.96.0.1        <none>        443/TCP          46m
primary-postgresql      LoadBalancer   10.105.10.137    <pending>     5432:30467/TCP   33m
replica-postgresql      ClusterIP      10.97.195.11     <none>        5432/TCP         7m17s
standalone-postgresql   ClusterIP      10.104.103.168   <none>        5432/TCP         2m34s
[root@lab01 postgresql-helm-charts]#
```

- Convert the standalone-postgresql to replica

```
cd /root/postgresql-helm-charts/chart-convert/templates
kubectl apply -f deployment-convert.yaml
```
- Get the pod logs and check if replica conversion completed, also login and check if data is replicated
  	
```
[root@lab01 templates]# kubectl logs standalone-postgresql-7454dbcbb7-v9ffz
Defaulted container "postgres" out of: postgres, pg-basebackup (init)

PostgreSQL Database directory appears to contain a database; Skipping initialization

2024-11-08 20:28:57.964 UTC [1] LOG:  starting PostgreSQL 17.0 (Debian 17.0-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
2024-11-08 20:28:57.965 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2024-11-08 20:28:57.965 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2024-11-08 20:28:57.966 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2024-11-08 20:28:57.969 UTC [36] LOG:  database system was interrupted; last known up at 2024-11-08 20:28:57 UTC
2024-11-08 20:28:57.983 UTC [36] LOG:  starting backup recovery with redo LSN 0/5000028, checkpoint LSN 0/5000080, on timeline ID 1
2024-11-08 20:28:57.983 UTC [36] LOG:  entering standby mode
2024-11-08 20:28:57.984 UTC [36] LOG:  redo starts at 0/5000028
2024-11-08 20:28:57.985 UTC [36] LOG:  completed backup recovery with redo LSN 0/5000028 and end LSN 0/5000120
2024-11-08 20:28:57.985 UTC [36] LOG:  consistent recovery state reached at 0/5000120
2024-11-08 20:28:57.985 UTC [1] LOG:  database system is ready to accept read-only connections
2024-11-08 20:28:57.995 UTC [37] LOG:  started streaming WAL from primary at 0/6000000 on timeline 1
[root@lab01 templates]#

[root@lab01 templates]# kubectl get pods
NAME                                     READY   STATUS    RESTARTS   AGE
primary-postgresql-66bd47f89-jnpnj       1/1     Running   0          37m
replica-postgresql-6484bfbf6f-4nh6f      1/1     Running   0          11m
standalone-postgresql-7454dbcbb7-v9ffz   1/1     Running   0          3s
[root@lab01 templates]#
[root@lab01 templates]# kubectl exec -it standalone-postgresql-7454dbcbb7-v9ffz -- su - postgres
Defaulted container "postgres" out of: postgres, pg-basebackup (init)
postgres@standalone-postgresql-7454dbcbb7-v9ffz:~$
postgres@standalone-postgresql-7454dbcbb7-v9ffz:~$
postgres@standalone-postgresql-7454dbcbb7-v9ffz:~$ psql
psql (17.0 (Debian 17.0-1.pgdg120+1))
Type "help" for help.

postgres=# \dt+
                                      List of relations
 Schema |  Name   | Type  |  Owner   | Persistence | Access method |    Size    | Description
--------+---------+-------+----------+-------------+---------------+------------+-------------
 public | authors | table | postgres | permanent   | heap          | 80 kB      |
 public | books   | table | postgres | permanent   | heap          | 7552 kB    |
 public | test    | table | postgres | permanent   | heap          | 8192 bytes |
(3 rows)

postgres=#
postgres=# select * from test;
 id | val
----+-----
  1 |   1
(1 row)

postgres=# delete from test;
ERROR:  cannot execute DELETE in a read-only transaction
postgres=#

```

### Restart the pod if required

```
[root@lab01 templates]# kubectl delete pods standalone-postgresql-7454dbcbb7-f6zdm
pod "standalone-postgresql-7454dbcbb7-f6zdm" deleted
[root@lab01 templates]#
```
## To push your folder to Git, follow these steps:

```
cd /root/postgresql-helm-charts
git init
git add .
git config --global user.email "postgrestraining@gmail.com"
git config --global user.name ""postgrestraining"
git commit -m "Initial commit with folder contents"

## Create a new repository on GitHub (for example., created helm-push repository)

## Push the folder
git remote add origin https://github.com/postgrestraining/helm-push.git
git push -u origin main
```
