# GitOps Task

## Overview

This repository contains the complete solution for the GitOps Task, covering application development, CI/CD, Docker, Kubernetes, scripting, and GitOps deployment using **FluxCD**.

The project is organized into three main directories:

```text
GitOps_Task/
├── Deliverables/
├── e-commerce-project-main/
└── gitops/
```

---

# Repository Structure

## 📁 Deliverables

This directory contains all required documentation, screenshots, and supporting files for each task.

```text
Deliverables/
├── CI/
├── Docker_Task/
├── Flux-CD/
├── kubernetes-cluster/
└── scripting/
```

### CI

Contains:

* GitLab CI/CD pipeline documentation
* Pipeline configuration
* Successful pipeline execution screenshots
* Dockerfile for the app
* Build, test, security scan, Docker build, image scan, and image push evidence

---

### Docker_Task

Contains:

* Dockerfile newman
* Docker image build documentation

---

### Flux-CD

Contains:

* FluxCD installation documentation
* GitOps repository configuration
* ImageRepository configuration
* ImagePolicy configuration
* ImageUpdateAutomation configuration
* Flux reconciliation screenshots
* Automatic deployment screenshots

---

### kubernetes-cluster

Contains:

* Kubernetes cluster setup Documentation
* Deployment manifest 
* Service manifest
* ingress manifest
* Running application screenshots
* Kubernetes deployment verification

---

### scripting

Contains:

* Python scripts

---

# e-commerce-project-main

This repository contains the e-commerce application and the complete GitLab CI/CD implementation.

Contents include:

* Application source code
* Dockerfile
* GitLab CI/CD pipeline
* Unit tests
* Dependency scanning
* Docker image build
* Docker image push to Docker Hub

For implementation details, refer to:

```text
e-commerce-project-main/README.md
```

---

# gitops

This repository contains the GitOps configuration used by FluxCD.

Contents include:

* Kubernetes manifests
* Flux bootstrap configuration
* ImageRepository
* ImagePolicy
* ImageUpdateAutomation
* Kustomizations

Flux continuously synchronizes the Kubernetes cluster with the manifests stored in this repository.

For detailed setup and configuration, refer to:

```text
gitops/README.md
```

---

# End-to-End Workflow

```text
Developer
    │
    │ Git Push
    ▼
GitLab Repository
    │
    ▼
GitLab CI/CD
    │
    ├── Build
    ├── Unit Tests
    ├── Dependency Scan
    ├── Docker Build
    ├── Image Scan
    ├── Push Image to Docker Hub
    ▼
Docker Hub
    │
    ▼
Flux ImageRepository
    │
    ▼
ImagePolicy
    │
    ▼
ImageUpdateAutomation
    │
Updates GitOps Repository
    │
    ▼
Flux GitRepository
    │
    ▼
Flux Kustomization
    │
    ▼
Kubernetes Cluster
```

---

# Technologies Used

* GitLab CI/CD
* Docker
* Docker Hub
* Kubernetes
* FluxCD
* GitOps
* Trivy
* Python

---

# Documentation

Each component contains its own detailed documentation:

| Directory                         | Description                                       |
| --------------------------------- | ------------------------------------------------- |
| `Deliverables/CI`                 | CI/CD documentation and screenshots               |
| `Deliverables/Docker_Task`        | Docker documentation and evidence                 |
| `Deliverables/Flux-CD`            | FluxCD setup, GitOps, and image automation        |
| `Deliverables/kubernetes-cluster` | Kubernetes deployment documentation               |
| `Deliverables/scripting`          | Automation scripts                                |
| `e-commerce-project-main`         | Application source code and GitLab CI/CD          |
| `gitops`                          | FluxCD GitOps repository and Kubernetes manifests |
