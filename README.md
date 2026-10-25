# AUCTOR: Autonomous Agent Authority Runtime

## Overview
AUCTOR is a portable, independently verifiable runtime for governing agent authority. It ensures that agents act only within cryptographically verifiable mandates.

## Installation
```bash
pip install -e .
```

## Quick Start
```bash
# 1. Initialize identity
auctor init

# 2. Issue mandate (Parent -> Child delegation)
auctor issue --subject agent_parent --tool read_file
auctor issue --subject agent_child --tool read_file --parent-file mandate_m_xxxx.json

# 3. Run tool & generate receipt
auctor run --mandate-file mandate_m_yyyy.json --tool read_file

# 4. Verify receipt
auctor verify --receipt-file receipt_m_yyyy_read_file.json
```

## Status: MVP Complete
- [x] Identity (Ed25519)
- [x] Mandate Protocol (JCS signed)
- [x] Attenuating Delegation
- [x] Evidence Receipts
- [x] Offline Verification
