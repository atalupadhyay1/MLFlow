import mlflow
import mlflow.pyfunc
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Configure MLflow db
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("custom_pyfunc_experiment")

# Define the Custom PyFunc model class
class ChurnThresholdClassifier(mlflow.pyfunc.PythonModel):
    """
    A custom MLflow PyFunc model wrapper.
    It takes an underlying trained classification model and applies a custom probability 
    threshold (e.g., 0.70) instead of the default 0.50. This is highly useful in production
    churn systems where we only want to flag accounts we are highly confident will churn.
    """
    def __init__(self, model, threshold=0.70):
        self.model = model
        self.threshold = threshold

    def load_context(self, context):
        # This method is executed when the model is loaded back into memory for serving
        pass

    def predict(self, context, model_input):
        # Convert input to DataFrame if it isn't one
        if isinstance(model_input, list):
            model_input = pd.DataFrame(model_input)
            
        # Get class probabilities
        probabilities = self.model.predict_proba(model_input)
        
        # Extract probability of churn (class 1)
        churn_probabilities = probabilities[:, 1]
        
        # Apply custom classification threshold
        predictions = (churn_probabilities >= self.threshold).astype(int)
        return predictions

if __name__ == "__main__":
    print("Training base model for custom PyFunc wrapping...")
    # Generate simple data
    X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train underlying model
    base_model = RandomForestClassifier(n_estimators=100, random_state=42)
    base_model.fit(X_train, y_train)
    
    # Wrap model with custom PyFunc class
    custom_model = ChurnThresholdClassifier(model=base_model, threshold=0.75)
    
    print("Logging custom PyFunc model to MLflow...")
    with mlflow.start_run(run_name="log_custom_pyfunc"):
        # Log the PyFunc model using mlflow.pyfunc.log_model
        # This creates a model folder containing python_model.pkl and conda configs
        mlflow.pyfunc.log_model(
            artifact_path="threshold_model",
            python_model=custom_model,
            input_example=X_test[:2]
        )
        
        print("\nSUCCESS: Custom PyFunc model logged to MLflow!")
