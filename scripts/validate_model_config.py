import yaml, sys

try:
    with open("model_config.yaml") as f:
        config = yaml.safe_load(f)
    assert "model" in config and "provider" in config
    print("✅ Model config is valid")
except Exception as e:
    print("❌ Model config error:", e)
    sys.exit(1)
