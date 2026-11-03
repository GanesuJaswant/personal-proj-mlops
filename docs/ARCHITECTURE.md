# System Architecture: End-to-End MLOps Car Price Prediction

```mermaid
flowchart TD
    subgraph Data Layer
        A[Raw Ingestion\nCarPrice_Assignment.csv] --> B[Validation Gate\n02_validate_data.py]
        B --> C[Preprocessing Pipeline\nColumnTransformer]
        C --> D[Data Partitions\nX_train, X_test, y_train, y_test]
    end

    subgraph Training & Registry Layer
        D --> E[Baseline Models\nDecisionTree, RandomForest]
        E --> F[MLflow Tracking\nMetrics, Params, Artifacts]
        F --> G[MLflow Model Registry\nCandidate Registration]
        G --> H[Quality Gate & Lifecycle\nChampion-Challenger]
    end

    subgraph Serving & Deployment Layer
        H --> I[Deployment Export\ndeployment/model.pkl]
        I --> J[Container Image\nDocker Multi-Stage]
        J --> K[Kubernetes Cluster\nReplicas & Service]
        K --> L[FastAPI App\nPOST /predict]
    end

    subgraph Continuous Monitoring Layer
        L --> M[Inference Telemetry\ninference_log.jsonl]
        M --> N[Drift Detection\nKS-Test, PSI, Concept Drift]
        N --> O{Drift Threshold Exceeded?}
        O -- Yes --> P[Automated Retraining Trigger]
        P --> C
        O -- No --> Q[Healthy Monitoring]
    end
```

## System Highlights
1. **Separation of Concerns**: Modular pipeline stages from 01 to 13.
2. **Reproducibility**: Parameterized random states, frozen transformer states, and explicit dependency management.
3. **Automated Governance**: Champion-Challenger promotion with strict $R^2 \ge 0.80$ quality gates.
4. **Cloud-Native Serving**: Containerized FastAPI service with real-time JSONL telemetry logging and health probes.
