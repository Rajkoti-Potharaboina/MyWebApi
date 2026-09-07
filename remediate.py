import subprocess

vulnerabilities = [
    {
        "id": "APP0001",
        "title": "Fix(APP0001): Resolve SQL Injection",
        "branch": "fix/app0001-sql-injection",
        "old_code": 'string query = "SELECT * FROM Users WHERE Username = \'" + username + "\'";',
        "new_code": 'string query = "SELECT * FROM Users WHERE Username = @Username"; // Parameterized query fix',
        "details": "Replaced string concatenation with parameterized query parameters."
    },
    {
        "id": "APP0002",
        "title": "Fix(APP0002): Resolve Cross-Site Scripting (XSS)",
        "branch": "fix/app0002-cross-site-scripting-(xss)",
        "old_code": 'string html = "<h1>User Output: " + input + "</h1>";',
        "new_code": 'string html = "<h1>User Output: " + System.Net.WebUtility.HtmlEncode(input) + "</h1>";',
        "details": "Sanitized user input rendering via HtmlEncode."
    },
    {
        "id": "APP0003",
        "title": "Fix(APP0003): Resolve Hardcoded Secret",
        "branch": "fix/app0003-hardcoded-secret",
        "old_code": 'string secretKey = "SuperSecretKey12345!";',
        "new_code": 'string secretKey = builder.Configuration["ApiKey"] ?? string.Empty;',
        "details": "Removed hardcoded API secret key and retrieved it from configuration."
    }
]

for vuln in vulnerabilities:
    print(f"\n--- Processing {vuln['id']}: {vuln['title']} ---")
    
    # Switch branch
    subprocess.run(["git", "checkout", "master"], check=True)
    subprocess.run(["git", "checkout", "-b", vuln["branch"]], check=True)
    
    # Modify Program.cs directly
    with open("Program.cs", "r", encoding="utf-8") as f:
        content = f.read()
    
    if vuln["old_code"] in content:
        content = content.replace(vuln["old_code"], vuln["new_code"])
        with open("Program.cs", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Applied patch to Program.cs for {vuln['id']}")
    else:
        print(f"Target pattern for {vuln['id']} not found in Program.cs (or already updated).")

    # Git Commit and Force Push
    subprocess.run(["git", "add", "Program.cs"], check=True)
    subprocess.run(["git", "commit", "-m", vuln["title"]], check=True)
    subprocess.run(["git", "push", "-u", "origin", vuln["branch"], "--force"], check=True)
    
    pr_cmd = [
        "gh", "pr", "create",
        "--title", vuln["title"],
        "--body", f"Automated fix generated for **{vuln['id']}**.\n\nDetails: {vuln['details']}",
        "--base", "master"
    ]
    subprocess.run(pr_cmd, check=True)
    print(f"Successfully created PR for {vuln['id']}")