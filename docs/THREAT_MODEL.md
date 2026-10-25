# AUCTOR Threat Model
- **Delegation Hijacking**: Child mandate must not be allowed to widen capabilities. (Mitigation: Attenuation Check)
- **Signature Forgery**: Mandates require Ed25519 signature verification before policy evaluation.
- **Receipt Substitution**: Each receipt is signed and linked to a mandate ID.
