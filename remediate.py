import json
import subprocess
import os

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
        return False
    return result.stdout.strip()

def process_vulnerabilities():
    # Load scan results
    with open('scan_results.json', 'r') as f:
        vulnerabilities = json.load(f)

    for vuln in vulnerabilities:
        vuln_id = vuln['id']
        vuln_type = vuln['vulnerability']
        target_file = vuln['file']
        details = vuln['details']

        branch_name = f"fix/{vuln_id.lower()}-{vuln_type.lower().replace(' ', '-')}"
        
        print(f"\n--- Processing {vuln_id}: {vuln_type} ---")
        
        # 1. Switch back to main and create a fix branch
        run_command("git checkout master || git checkout main")
        run_command(f"git checkout -b {branch_name}")

        # 2. Prompt Claude CLI to fix the file directly
        prompt = (
            f"Fix the {vuln_type} vulnerability ({vuln_id}) in {target_file}. "
            f"Details: {details}. "
            f"Modify {target_file} in place and ensure it compiles."
        )
        print(f"Running Claude CLI for {vuln_id}...")
        run_command(f'claude -p "{prompt}"')

        # 3. Stage, commit, and create GitHub PR
        run_command(f"git add {target_file}")
        run_command(f'git commit -m "fix({vuln_id}): resolve {vuln_type}"')
        run_command(f"git push -u origin {branch_name}")
        
        pr_title = f"Fix({vuln_id}): Resolve {vuln_type}"
        pr_body = f"Automated fix generated via Claude CLI for **{vuln_id}** ({vuln_type}).\n\nDetails: {details}"
        run_command(f'gh pr create --title "{pr_title}" --body "{pr_body}" --base master')

        print(f"Successfully created PR for {vuln_id}")

if __name__ == "__main__":
    process_vulnerabilities()