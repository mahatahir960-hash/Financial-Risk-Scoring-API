"""Small reproducible portfolio project using synthetic, non-sensitive data."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report

def train(seed=42):
    x, y = make_classification(n_samples=1200, n_features=8, n_informative=5, weights=[0.85, 0.15], random_state=seed)
    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, random_state=seed)
    model = RandomForestClassifier(n_estimators=80, max_depth=6, random_state=seed)
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    return model, x_test, y_test, probabilities

def run():
    model, x, y, pred = train()
    print(f"ROC AUC: {roc_auc_score(y, pred):.3f}")

def serve():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import json
    model, _, _, _ = train()
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path != "/score":
                self.send_error(404); return
            try:
                n = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(n))
                features = np.asarray(payload["features"], dtype=float).reshape(1, -1)
                if features.shape[1] != 8: raise ValueError("Expected 8 numeric features")
                result = json.dumps({"risk_score": float(model.predict_proba(features)[0, 1])}).encode()
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(result)
            except (ValueError, KeyError, TypeError) as exc:
                self.send_error(400, str(exc))
    print("Serving POST /score on http://127.0.0.1:8080")
    HTTPServer(("127.0.0.1", 8080), Handler).serve_forever()

if __name__ == "__main__":
    serve()
