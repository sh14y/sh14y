import os
import re
import json

class PiClawToolkit:
    """
    Professional AI Security & Data Refinement Toolkit.
    Showcasing capabilities in Security Audit (Skill A) and Data Cleaning (Skill B/C).
    """
    
    def __init__(self):
        # Patterns for security audit (Skill A)
        self.threat_patterns = [
            r'ghp_[a-zA-Z0-9]{36}',           # GitHub Tokens
            r'moltbook_sk_[a-zA-Z0-9_-]+',    # Moltbook Keys
            r'https://webhook\.site/[a-z0-9-]+', # Exfiltration Endpoints
            r'eval\(',                         # Dangerous Execution
            r'exec\('                          # Dangerous Execution
        ]

    def audit_directory(self, path):
        """Scans a directory for security risks."""
        print(f"🛡️ Starting Security Audit on: {path}")
        findings = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(('.py', '.md', '.env', '.json')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            for pattern in self.threat_patterns:
                                if re.search(pattern, content):
                                    findings.append({"file": file, "risk": pattern})
                    except Exception as e:
                        continue
        return findings

    def refine_data(self, input_json):
        """Performs data cleaning and refinement (Skill B/C)."""
        # Simulate cleaning up messy agent logs or data
        try:
            data = json.loads(input_json)
            refined = []
            for entry in data:
                # Clean up whitespace and capitalize keys
                clean_entry = {k.strip().upper(): v.strip() if isinstance(v, str) else v for k, v in entry.items()}
                refined.append(clean_entry)
            return refined
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    toolkit = PiClawToolkit()
    
    # 1. Test Data Refinement
    sample_data = '[{" name ":" Elvis ","status":"  active "}, {" name":"Pi_Claw ","status":"hunting"}]'
    print("📊 Data Refinement Test:")
    print(toolkit.refine_data(sample_data))
    
    # 2. Test Security Audit (on its own file)
    print("\n🛡️ Security Audit Test:")
    results = toolkit.audit_directory("./portfolio/toolkit")
    if not results:
        print("✅ No immediate threats detected in test file.")
    else:
        print(f"⚠️ Findings: {results}")

