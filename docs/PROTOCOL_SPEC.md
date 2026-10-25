# AUCTOR Protocol Specification v0.1.0-draft

## 1. Identity
- **Algorithm**: Ed25519
- **Identifier**: `did:auctor:<pubkey_hex>`

## 2. Mandate Structure
A Mandate is a signed statement of authority.

```json
{
  "type": "mandate",
  "version": "0.1.0",
  "id": "m_...",
  "issuer": "did:auctor:...",
  "subject": "did:auctor:...",
  "audience": "runtime.auctor.local",
  "expires": 1730000000,
  "not_before": 1720000000,
  "nonce": "unique_string",
  "parent_id": null,
  "capabilities": {
    "tools": ["read_file", "write_file"],
    "resources": {
      "path_prefix": "/home/agent/workspace"
    }
  },
  "signature": {
    "pubkey": "...",
    "value": "..."
  }
}
```

## 3. Evidence Receipt
A Receipt proves an action was taken under a specific mandate.

```json
{
  "type": "receipt",
  "id": "r_...",
  "mandate_id": "m_...",
  "runtime_id": "did:auctor:...",
  "timestamp": 1729862400,
  "action": {
    "tool": "write_file",
    "args_hash": "sha256:...",
    "call_id": "..."
  },
  "outcome": {
    "status": "success",
    "result_hash": "sha256:..."
  },
  "signature": {
    "pubkey": "...",
    "value": "..."
  }
}
```

## 4. Verification Logic
A receipt is **VALID** if and only if:
1. All signatures are valid (Ed25519 over JCS-canonicalized JSON).
2. The `mandate_id` in the receipt matches a valid mandate.
3. The mandate has not expired.
4. The `action.tool` is present in the mandate's `capabilities.tools`.
5. (If delegation) The entire chain of mandates from the root issuer is valid and attenuating.
