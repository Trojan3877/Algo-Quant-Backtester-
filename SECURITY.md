# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| `main`  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it by emailing security@your-domain.com. Include:

- A clear, concise description of the vulnerability.
- Steps to reproduce the issue.
- Your environment details (OS, Python version, etc.).
- Any suggested fixes or workarounds.

## Response Process

1. **Acknowledgement** within 24 hours.  
2. **Investigation** and risk assessment.  
3. **Fix and Disclosure**: a patch release will be issued, followed by a public advisory.  
4. **Resolution**: issue a disclosure timeline and credit the reporter (unless anonymity is requested).

## Secure Development Practices

- All dependencies are regularly scanned with CodeQL and third-party tools (e.g., Snyk).  
- Infrastructure-as-Code is validated with `terraform validate` and `ansible-lint`.  
- Continuous integration includes security checks in `.github/workflows/codeql.yml`.  

## Reporting Options

- For sensitive issues, please use the email above.  
- For general questions or low-severity reports, feel free to open a GitHub issue labeled `security`.  
