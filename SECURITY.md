# Security Policy

Security is a foundational pillar of **Auth_forge**. We take vulnerabilities and reporting seriously to maintain the safety of user credentials and tokens.

---

## Supported Versions

| Version | Supported |
| :--- | :--- |
| `1.x.x` (Current Main) | :white_check_mark: |
| `< 1.0.0` | :x: |

---

## Reporting a Vulnerability

If you discover a security vulnerability within Auth_forge:

1. **Do not create a public GitHub issue.**
2. Send an email to the repository maintainer or open a private GitHub Security Advisory.
3. Include detailed reproduction steps, potential impact, and system configuration.
4. Allow reasonable time for investigation and patch deployment prior to public disclosure.

---

## Security Best Practices for Deployment

When running Auth_forge in staging or production environments, adhere to the following recommendations:

1. **Generate Cryptographically Secure JWT Keys**:
   Never use default or placeholder strings. Generate a 256-bit or 512-bit secret:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. **Use HTTPS / TLS**:
   Always serve traffic behind an SSL termination proxy (e.g. Nginx, Caddy, Cloudflare, AWS ALB) so tokens and credentials are encrypted in transit.
3. **Database Security**:
   - Avoid using the default `postgres` superuser for application connections.
   - Restrict database firewall access to only the backend host.
4. **Token Expiration Policy**:
   - Keep `ACCESS_TOKEN_EXPIRE_MINUTES` short (e.g. 15 minutes) to minimize exposure windows if a token is compromised.
5. **CORS Restrictions**:
   - Ensure FastAPI CORS middleware explicitly whitelists only trusted origins before exposing frontend-backend communication across domains.
6. **Password Hashing**:
   - Auth_forge uses **Argon2** (via `pwdlib`), which is resistant to GPU-based brute-force attacks. Do not revert to legacy hashing schemes like MD5 or plain SHA-256.
