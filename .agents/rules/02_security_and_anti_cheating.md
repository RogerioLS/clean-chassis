# 02 — Security, Secret Hygiene & Anti-Leak

1. **Zero Committed Secrets**: Never commit API keys, personal access tokens, private keys, or passwords.
2. **Ignored Credentials**: `kaggle.json`, `.kaggle/`, `.env*`, `*token*`, and `*.key` must remain in `.gitignore`.
3. **SSL & Proxy Resilience**: Local scripts contacting APIs must be resilient to corporate SSL inspection proxies using safe unverified fallbacks or `REQUESTS_CA_BUNDLE`.
4. **Hermetic Mocks**: Unit tests must use mock fixtures and never depend on live external network endpoints.
