# GenAi Project

A sample end-to-end workflow for creating a Python Flask application that interacts with Google AI (Gemini) and deploying it to Google Kubernetes Engine (GKE) using CI/CD.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Create an API Key using Google AI Studio](#step-1-create-an-api-key-using-google-ai-studio)
  - [1. Create an API Key](#1-create-an-api-key)
  - [2. Securely Store the API Key](#2-securely-store-the-api-key)
  - [3. Authenticate with the API](#3-authenticate-with-the-api)
  - [4. Enable API Services](#4-enable-api-services)
- [Step 2: Create a Python–Flask App](#step-2-create-a-pythonflask-app)
  - [Frontend Integration](#frontend-integration)
- [Step 3: Create a CI/CD Pipeline for GKE Deployment](#step-3-create-a-cicd-pipeline-for-gke-deployment)
  - [Dockerfile](#dockerfile)
  - [Kubernetes Manifests](#kubernetes-manifests)
  - [Skaffold Configuration](#skaffold-configuration)
  - [Cloud Build](#cloud-build)
  - [Cloud Deploy](#cloud-deploy)
  - [Verification](#verification)
- [Troubleshooting Kubernetes Deployments](#troubleshooting-kubernetes-deployments)
  - [Common Issues and Resolutions](#common-issues-and-resolutions)
- [Contributing](#contributing)

---
## Project Structure

app.py: Main Flask application.
templates/index.html: Frontend HTML for the Flask app.
kubernetes.yaml: Kubernetes manifest (alternative to environment-specific manifests).
dev-target.yaml / prod-target.yaml: Separate environment-based Kubernetes manifests.
cloudbuild.yaml: Defines the build and push steps for Docker images and triggers your deployment.
clouddeploy.yaml: Defines the Cloud Deploy pipeline for different stages (dev, prod).
skaffold.yaml: Outlines build and deployment settings for multiple environments.
Dockerfile: Defines how to build the Docker image for the Flask application.



## Prerequisites

- A Google Cloud Platform account  
- `gcloud` (Google Cloud CLI) installed and authenticated  
- A Kubernetes cluster on GKE (or permission to create one)  
- A GitHub repository (public or private)  
- (Optional) A set-up environment in Google AI Studio  

---

## Step 1: Create an API Key using Google AI Studio

### 1. Create an API Key

- Navigate to **Google AI Studio** in the GCP console.  
- Select or create a new GCP project.  
- Create a new **API Key** to use for Gemini.  

### 2. Securely Store the API Key

- **Option 1**: Store the key as an environment variable (e.g., using `export`).  
- **Option 2**: Use a secret manager (like Google Secret Manager) to store it securely.  

### 3. Authenticate with the API

- Use your API key (or service account JSON credentials) in the application.  

### 4. Enable API Services

- Ensure APIs needed (e.g., AI Platform, Cloud Build, Cloud Deploy) are enabled in the GCP console.  

---

## Step 2: Create a Python–Flask App

1. Install dependencies listed in `requirements.txt`.  
2. Develop the Flask application in `app.py` to handle routes for:
   - Root endpoint returning the HTML template.  
   - Additional endpoints for sending requests to Gemini (if applicable).  
3. **Frontend Integration** using the `index.html` template to capture user inputs and display results.  

### Frontend Integration

- Add a form or UI components in `templates/index.html` to interact with the Flask routes.  

---

## Step 3: Create a CI/CD Pipeline for GKE Deployment

### Dockerfile

- A Docker configuration that sets up the Python environment, installs dependencies, and runs the Flask app.  

### Kubernetes Manifests

- `dev-target.yaml` and `prod-target.yaml` for separate namespaces and resource definitions in GKE.  
- Allows different environment variables, replicas, or resource allocations for dev vs. prod.  

### Skaffold Configuration

- A manifest (`skaffold.yaml`) to automate building and deploying to Kubernetes across different environments.  

### Cloud Build

- A file (`cloudbuild.yaml`) that defines the steps to:  
  - Build and push the Docker image to Container Registry (or Artifact Registry).  
  - Deploy updates to the dev environment (e.g., by updating the container image in the deployment).  

### Cloud Deploy

- A pipeline (`clouddeploy.yaml`) that orchestrates progressive rollouts from dev to prod, potentially requiring manual approvals.  

### Verification

1. Create a **Trigger** in Cloud Build linked to the GitHub repository.  
2. Push changes to GitHub and verify:
   - The build is triggered.  
   - The pipeline successfully builds the Docker image and applies the Kubernetes manifests.  
3. Check GKE for new pods and services in both dev and prod namespaces.  
4. Access the LoadBalancer IP or external endpoint to validate the application is working.  

---

## Troubleshooting Kubernetes Deployments

### Common Issues and Resolutions

#### Pods in CrashLoopBackOff State
- **Cause**: The application might be crashing on startup.  
- **Resolution**:
  - Verify your application’s runtime logs to identify errors (e.g., incorrect environment variables or missing dependencies).  
  - Ensure the port in your application logic matches the container port specified in the Kubernetes manifest.  

#### Pods in ImagePullBackOff State
- **Cause**: Kubernetes cannot pull the container image.  
- **Resolution**:
  - Check if the image name, tag, or registry is correct.  
  - Ensure the image is pushed to the container registry (e.g., `gcr.io/<project_id>`) under the correct project.  
  - Verify permissions to pull the image.  

#### Service Not Assigning an External IP
- **Cause**: The LoadBalancer service may be pending or not provisioned.  
- **Resolution**:
  - Confirm the service type is LoadBalancer.  
  - In the GCP console, verify if a forwarding rule is created for your service.  
  - Check if you have sufficient quota for load balancers.  

#### No External Access to the App
- **Cause**: Firewall rules or security policies may be blocking traffic.  
- **Resolution**:
  - Ensure your GKE cluster has the correct firewall rules allowing external traffic on the exposed port.  
  - Validate the external IP is correctly assigned to the LoadBalancer service.  

#### Namespace Issues
- **Cause**: Resources might be deployed in the wrong namespace, or you’re using the wrong namespace context.  
- **Resolution**:
  - Confirm that the namespace in your manifest is the same one you’re querying.  
  - Use proper namespace context in `kubectl` commands (e.g., `kubectl get pods -n dev-target`).  

#### Resource Limit Conflicts
- **Cause**: CPU or memory limits might be too high or too low, causing pods to fail.  
- **Resolution**:
  - Adjust resource requests/limits in your manifests.  
  - Monitor pod usage with `kubectl top` or GCP’s metrics to ensure adequate resources.  

#### Event Logs and Debugging
- **Action**:
  - Describe resources to see event logs (e.g., `kubectl describe pod <pod_name>`).  
  - Check container logs to find runtime errors (e.g., `kubectl logs <pod_name>`).  
  - Explore GCP’s Cloud Logging for additional debugging information.  

---

## Contributing

Feel free to open issues or submit pull requests for improvements and suggestions.

---

