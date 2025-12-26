import json
import os
import datetime
from config import LOG_DIR

class DebateLogger:
    def __init__(self, log_file_path=None):
        if log_file_path:
            self.log_file_path = log_file_path
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file_path = os.path.join(LOG_DIR, f"debate_log_{timestamp}.jsonl")
        
        # Ensure the file is created/cleared
        with open(self.log_file_path, 'w') as f:
            pass

    def log(self, event_type, data):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        with open(self.log_file_path, 'a') as f:
            f.write(json.dumps(entry) + "\n")

# Global logger instance (can be re-initialized if needed)
logger = DebateLogger()
