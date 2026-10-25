# Competitive Landscape: Agent Authorization & Verifiability

AUCTOR sits at the intersection of agent governance, cryptographic authorization, and verifiable execution.

| Project | Approach | Trust Model | Verifiability | Delegation |
| :--- | :--- | :--- | :--- | :--- |
| **AGP** | Protocol layer for intent declaration | Logic-based enforcement | Signed receipts & ledger | Capability tokens |
| **MANDATE** | ZK-policy for financial actions | ZK-proofs of rule compliance | Cryptographic receipts | Fixed rules |
| **VeriTask** | TEE-based task execution | Hardware (Intel TDX) + zkTLS | ProofBundles | Enclave-to-Enclave |
| **AgentProof**| Compiler & Simulator | Static analysis & Red-teaming | No execution receipts | Scope propagation |
| **AUCTOR** | **Proof-Carrying Runtime** | **Deterministic enforcement** | **Portable signed evidence** | **Attenuating Delegation** |

## Differentiation Hypotheses

1. **Portable Evidence**: AUCTOR receipts are self-contained and verifiable offline by any third party without access to the original runtime or a blockchain.
2. **Attenuating Delegation**: AUCTOR provides first-class support for "narrowing" authority as it moves from human -> agent -> sub-agent, enforced by signature-linked mandates.
3. **Model-Agnostic Boundary**: Enforcement happens at the tool-execution boundary, making it compatible with any LLM/framework (via MCP).

## Research Questions
- How to handle "budgets" (tokens, time, money) in a portable, stateless receipt?
- Can we achieve meaningful verification without TEEs by using "Reproducible Tool Call" hashes?
- What is the minimal metadata required to prove a delegation chain is valid?

Sources:
- [AGP Protocol](https://github.com/cunardai/agp-protocol) (Retrieved: 2026-10-25)
- [MANDATE](https://www.mandate.help/) (Retrieved: 2026-10-25)
- [AgentProof](https://github.com/evanl666/agentproof) (Retrieved: 2026-10-25)
- [VeriTask](https://github.com/Skottbie/VeriTask) (Retrieved: 2026-10-25)
