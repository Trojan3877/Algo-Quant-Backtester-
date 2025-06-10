# System Architecture

This document outlines the end-to-end architecture of the **AlgoQuant Backtester & Signal Engine** platform.

```mermaid
flowchart LR
  subgraph Data Layer
    SF[Snowflake] --> RawData[data/raw/spy.parquet]
    Kafka[(Kafka Topics)] --> TickData[data/raw/tick.parquet]
  end

  subgraph Processing Layer
    RawData --> FE[Feature Engineering]
    TickData --> FE
    FE --> Features[data/processed/features.csv]
  end

  subgraph Modeling Layer
    Features --> TFModel[TensorFlow LSTM Model]
    Features --> RLAgent[PyTorch DQN Agent]
    TFModel --> Models[models/*.h5, .pth]
    RLAgent --> Models
  end

  subgraph Backtesting & Versioning
    Models --> Backtest[Backtesting Engine]
    Backtest --> Results[backtest/results.csv]
    Features & Models & Code --> DVC[DVC Pipeline]
  end

  subgraph Deployment Layer
    Models --> API[FastAPI Service]
    API --> Docker[Docker Container]
    Docker --> K8s[Kubernetes Cluster]
    K8s --> Helm[Helm Chart]
    K8s --> HPA[HPA Autoscaler]
    K8s --> Ingress[Ingress Controller]
  end

  subgraph CI/CD & Infra as Code
    GitHubActions --> DVC
    GitHubActions --> Docker
    GitHubActions --> Terraform[Terraform IaC]
    GitHubActions --> Helm
    GitHubActions --> Ansible[Ansible Automation]
    Terraform --> AWS[AWS (EKS, S3, IAM)]
  end

  subgraph Monitoring & Tracking
    API --> Prom[Prometheus]
    API --> Graf[Grafana]
    Models --> MLflow[MLflow Tracking]
  end
