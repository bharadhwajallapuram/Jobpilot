import os, toml, pathlib

def load_config():
    path = pathlib.Path("config.toml")
    if not path.exists():
        path = pathlib.Path("config.example.toml")
    cfg = toml.load(path)
    # Env overrides
    cfg.setdefault("openai", {})["api_key"] = os.getenv("OPENAI_API_KEY", cfg["openai"].get("api_key", ""))
    return cfg