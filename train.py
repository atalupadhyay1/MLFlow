import mlflow
import optuna
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Step 1: Configure MLflow Tracking backend
# Using a local SQLite database file saves run details and metrics persistently.
# This prevents data loss when python terminates.
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Step 2: Establish the Experiment
experiment_name = "customer_churn_random_forest"
mlflow.set_experiment(experiment_name)

# Step 3: Prepare Synthetic Dataset
# Simulates churn prediction with 10 features
X, y = make_classification(
    n_samples=2000,
    n_features=10,
    n_informative=7,
    n_redundant=3,
    random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Define Optuna Objective Function
def objective(trial):
    # Suggest tree structure hyperparameters
    n_estimators = trial.suggest_int("n_estimators", 50, 250, step=50)
    max_depth = trial.suggest_int("max_depth", 3, 12)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 8)
    
    # Run each trial in a nested MLflow run under a parent execution
    run_name = f"trial_{trial.number}_n_{n_estimators}_d_{max_depth}"
    with mlflow.start_run(run_name=run_name, nested=True):
        # 1. Instantiate and fit RandomForest
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # 2. Evaluate performance
        preds = model.predict(X_test)
        accuracy = accuracy_score(y_test, preds)
        precision = precision_score(y_test, preds)
        recall = recall_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        
        # 3. Log Parameters to MLflow
        mlflow.log_params({
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split
        })
        
        # 4. Log Metrics to MLflow
        mlflow.log_metrics({
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        })
        
        # 5. Log Model Artifact
        # input_example sets the expected JSON payload signature schema for the API serving step
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="random_forest_model",
            input_example=X_test[:2]
        )
        
    return f1

if __name__ == "__main__":
    print(f"Starting Hyperparameter Optimization under experiment: '{experiment_name}'...")
    
    # Start parent run to group the tuning process
    with mlflow.start_run(run_name="optuna_parent_tuning"):
        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=5)
        
        best_params = study.best_params
        best_value = study.best_value
        
        print("\n--- Hyperparameter Optimization Complete ---")
        print(f"Best Trial F1-Score: {best_value:.4f}")
        print(f"Best Hyperparameters: {best_params}")
        
        # Log best summary parameters to the parent run
        mlflow.log_params(best_params)
        mlflow.log_metric("best_f1_score", best_value)
