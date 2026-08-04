# FluxCD Image Automation (Git-Based)

This project uses **FluxCD GitOps** to automatically deploy new Docker image versions to a Kubernetes cluster.

---

# Architecture

```text
Developer
    │
    │ git push
    ▼
GitLab CI/CD
    │
    ├── Build Docker Image
    ├── Push Docker Image → Docker Hub
    ▼
Docker Hub
    │
    ▼
Flux ImageRepository
    │
    ▼
Flux ImagePolicy
    │
    ▼
Flux ImageUpdateAutomation
    │
Updates deployment.yaml in Git
    │
    ▼
Git Repository (Source of Truth)
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

# Manifest Source of Truth

The Git repository acts as the **single source of truth** for the Kubernetes cluster. All Kubernetes manifests are stored in Git, and Flux continuously reconciles the cluster state to match the repository.

Repository structure:

```text
gitops/
├── apps/
│   └── ecommerce/
│       ├── deployment.yaml
│       ├── image-repository.yaml
│       ├── image-policy.yaml
│       ├── image-update.yaml
│       └── kustomization.yaml
│
└── clusters/
    └── local/
        ├── kustomization.yaml
        └── flux-system/
            ├── gotk-components.yaml
            ├── gotk-sync.yaml
            └── kustomization.yaml
```

---

# Flux Installation

Bootstrap Flux against the GitLab repository:

```bash
flux bootstrap gitlab \
  --owner=sabreensalama9 \
  --repository=gitops \
  --branch=main \
  --path=clusters/local \
  --hostname=gitlab.com \
  --token-auth
```

This installs the following Flux controllers:

- Source Controller
- Kustomize Controller
- Notification Controller
- Image Reflector Controller
- Image Automation Controller

---

# Configure Image Automation

## ImageRepository

The `ImageRepository` resource periodically scans Docker Hub for new image tags.

```yaml
apiVersion: image.toolkit.fluxcd.io/v1
kind: ImageRepository
metadata:
  name: ecommerce
  namespace: flux-system
spec:
  image: docker.io/sabreensalama/ecommerce
  interval: 1m
```

---

## ImagePolicy

The `ImagePolicy` resource selects the latest image according to the configured policy.

```yaml
apiVersion: image.toolkit.fluxcd.io/v1
kind: ImagePolicy
metadata:
  name: ecommerce
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: ecommerce
  policy:
    numerical:
      order: asc
```

Example available tags:

```text
1
2
3
...
25
```

Flux automatically selects:

```text
25
```

---

## ImageUpdateAutomation

The `ImageUpdateAutomation` resource updates the deployment manifest in Git whenever a newer image is detected.

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageUpdateAutomation
metadata:
  name: ecommerce
  namespace: flux-system
spec:
  interval: 1m

  sourceRef:
    kind: GitRepository
    name: flux-system

  git:
    checkout:
      ref:
        branch: main

    commit:
      author:
        name: Flux
        email: flux@example.com

      messageTemplate: |
        Update image to {{range .Changed.Changes}}{{println .NewValue}}{{end}}

    push:
      branch: main

  update:
    strategy: Setters
    path: ./apps/ecommerce
```

Whenever a new image is pushed to Docker Hub:

```text
docker.io/sabreensalama/ecommerce:42
```

Flux automatically updates the deployment manifest:

```yaml
image: docker.io/sabreensalama/ecommerce:42
```

commits the change to Git, and triggers a deployment.

---

# GitLab CI/CD Pipeline

The GitLab pipeline performs the following stages:

```text
Build
    │
    ▼
Unit Tests
    │
    ▼
Dependency Scan
    │
    ▼
Docker Build
    │
    ▼
Image Scan
    │
    ▼
Docker Push
    │
    ▼
Flux detects new image
    │
    ▼
Flux updates Git
    │
    ▼
Flux deploys automatically
```

The CI pipeline is only responsible for building, testing, scanning, and pushing the Docker image.

It **does not execute `kubectl apply`**.

Deployment is handled entirely by FluxCD.

---

# How Flux Image Automation Works

1. The developer pushes application code to GitLab.
2. GitLab CI builds a new Docker image.
3. The image is pushed to Docker Hub using a new version tag.
4. Flux `ImageRepository` periodically scans Docker Hub for new image tags.
5. `ImagePolicy` evaluates the available tags and selects the latest one based on the configured policy.
6. `ImageUpdateAutomation` updates the Kubernetes deployment manifest in the Git repository with the selected image tag.
7. Flux commits and pushes the updated manifest to the Git repository.
8. The `GitRepository` source detects the new commit.
9. The `Kustomization` reconciles the updated manifests and applies them to the Kubernetes cluster.
10. Kubernetes performs a rolling update of the Deployment using the new container image.

---

# Deployment Failure and Rollback

Flux continuously compares the cluster state with the Git repository and ensures they remain synchronized.

If a deployment fails:

- Kubernetes keeps the previous healthy ReplicaSet available.
- Failed Pods are restarted according to the Deployment strategy.
- Flux continues reconciling the desired state but does not automatically roll back to a previous image.

To perform a rollback:

1. Revert the Git commit that updated the image tag.
2. Push the reverted commit to the Git repository.
3. Flux detects the new Git revision.
4. Flux reconciles the updated manifests.
5. Kubernetes performs a rolling update back to the previous stable image version.

This Git-based rollback approach provides:

- Complete version history
- Full audit trail
- Declarative infrastructure
- Predictable and repeatable deployments

---

# Advantages of This Approach

- Uses **FluxCD only** for deployment automation.
- Implements a **GitOps** workflow.
- Uses Git as the **single source of truth**.
- Automatically deploys newly published Docker images.
- Provides fully declarative Kubernetes deployments.
- Maintains a complete deployment history in Git.
- Supports simple and reliable rollbacks through Git commits.
- Suitable for production and multi-environment Kubernetes deployments.