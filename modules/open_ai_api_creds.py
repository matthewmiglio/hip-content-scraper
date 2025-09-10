import os
import json

class OpenAICreds:
    def __init__(self, creds_path: str = "open_ai_api_creds.json"):
        """
        Loads OpenAI API credentials from a JSON file.
        If the file does not exist, initializes it with a placeholder.
        """
        self.creds_path = creds_path
        self.api_key = None
        self._load_or_init()

    def _load_or_init(self):
        if not os.path.exists(self.creds_path):
            # File does not exist -> create placeholder
            placeholder = {"api_key": "YOUR_API_KEY_HERE"}
            with open(self.creds_path, "w", encoding="utf-8") as f:
                json.dump(placeholder, f, indent=2)
            print(f"[OpenAICreds] Created placeholder creds file at '{self.creds_path}'. "
                  "Please update it with your real API key.")
            self.api_key = placeholder["api_key"]
        else:
            try:
                with open(self.creds_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.api_key = data.get("api_key")
                if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
                    print(f"[OpenAICreds] Warning: creds file at '{self.creds_path}' "
                          "contains a placeholder or empty key. Please update it.")
            except (json.JSONDecodeError, IOError) as e:
                print(f"[OpenAICreds] Error reading creds file: {e}")
                self.api_key = None

    def get_open_api_key(self) -> str | None:
        """Return the API key string (may be None or placeholder)."""
        return self.api_key
