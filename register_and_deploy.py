import mlflow
from mlflow.tracking import MlflowClient

# Step 1: Configure backend
mlflow.set_tracking_uri("sqlite:///mlflow.db")
client = MlflowClient()

# Step 2: Query database for the best model run
experiment_name = "customer_churn_random_forest"
experiment = client.get_experiment_by_name(experiment_name)

if not experiment:
    print(f"[ERROR] Experiment '{experiment_name}' not found. Please run train.py first to populate database.")
    exit()

# Search for the run with the highest evaluation F1-score
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1_score DESC"],
    max_results=1
)

if not runs:
    print("[ERROR] No runs found inside the experiment database.")
    exit()

best_run = runs[0]
best_run_id = best_run.info.run_id
best_f1 = best_run.data.metrics["f1_score"]

print(f"Found Best Run ID: {best_run_id}")
print(f"F1-Score of Best Run: {best_f1:.4f}")

# Step 3: Register Model dynamically in Central Registry
model_name = "CustomerChurnClassifier"
model_uri = f"runs:/{best_run_id}/random_forest_model"

print(f"Registering model version under registry namespace '{model_name}'...")
model_version = mlflow.register_model(model_uri=model_uri, name=model_name)
print(f"Successfully registered version {model_version.version}!")

# Step 4: Programmatically transition model stage to 'Production'
# The archive_existing_versions flag automatically moves older Production models to 'Archived'
print(f"Promoting version {model_version.version} to 'Production'...")
client.transition_model_version_stage(
    name=model_name,
    version=model_version.version,
    stage="Production",
    archive_existing_versions=True
)

print("\n--- Model Staging Promotion Complete ---")
print(f"Model Name: {model_name}")
print(f"Active Production Version: {model_version.version}")
print(f"Stage: Production")
