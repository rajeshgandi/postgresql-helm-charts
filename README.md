# PostgreSQL Helm Charts

This repository contains Helm charts for deploying various configurations of PostgreSQL databases on Kubernetes. The charts included are:

- **Primary PostgreSQL** (`chart-primary/`): Deploys a standalone primary PostgreSQL instance.
- **Replica PostgreSQL** (`chart-replica/`): Deploys a replica PostgreSQL instance that syncs with a primary.
- **Standalone PostgreSQL** (`chart-fstandalone/`): Deploys a standalone PostgreSQL instance.
- **Standalone to Replica Conversion** (`chart-convert/`): Converts a standalone PostgreSQL instance to a replica.

## Chart Descriptions and Usage

### Repository structure
```
postgresql-helm-charts/
├── chart-primary/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── pv.yaml
│       ├── pvc.yaml
│       ├── service.yaml
│       └── deployment.yaml
├── chart-replica/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── pv.yaml
│       ├── pvc.yaml
│       ├── service.yaml
│       └── deployment.yaml
├── chart-standalone/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── pv.yaml
│       ├── pvc.yaml
│       ├── service.yaml
│       └── deployment.yaml
├── chart-convert/
│   ├── Chart.yaml
│   └── templates/
│       └── deployment-convert.yaml
└── README.md
```

For set-up instructions [click here](https://github.com/postgrestraining/postgresql-helm-charts/blob/main/Setup-instructions.md)


