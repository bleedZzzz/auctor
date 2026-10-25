# PRD: AUCTOR MVP

## Vision
Build a proof-carrying agent runtime where every action is backed by a signed mandate and produces a verifiable evidence receipt.

## Target User
Developers building autonomous coding agents or multi-agent systems who need to restrict authority and audit outcomes.

## MVP Scope (Phase 1)
- **Identity**: Create and manage Ed25519 keys for humans and agents.
- **Mandates**: 
    - Issue signed mandates with `allowlist` of tools.
    - Support `attenuating delegation` (child mandate narrower than parent).
- **Runtime Enforcement**: 
    - A deterministic policy engine that checks signatures and constraints.
    - Rejects any tool call not explicitly permitted.
- **Evidence**:
    - Generate signed "Evidence Receipts" for every successful action.
    - Receipts hash the action inputs and outputs for integrity.
- **Verifier**:
    - A CLI command to verify an evidence bundle offline.

## Non-Goals for MVP
- Browser/GUI (CLI only).
- Remote attestation (TEE).
- ZK-proofs.
- Real blockchain integration (Local-only roots).
- Token/Speculation.

## Acceptance Criteria
1. `auctor identity create` generates a keypair.
2. `auctor mandate issue` creates a signed constraint.
3. `auctor run --mandate <id>` executes a permitted tool.
4. `auctor run --mandate <id>` fails on an unpermitted tool.
5. `auctor verify <receipt>` returns "Valid" only if signatures and hashes match.
