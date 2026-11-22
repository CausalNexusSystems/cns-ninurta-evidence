# CNS NINURTA — public trial evidence (formerly AXIOM)

NINURTA is a fail-closed execution-authority kernel for autonomous agents developed by Causal Nexus Systems LLC.
Until November 2026 it was called **AXIOM**; the files below were produced and sealed under that name and are published
byte for byte, so they still say AXIOM. Nothing in them was edited after sealing.

**Paper:** Moreno, A. (2026). *Witnessed Anchors: Single-Use Authority for Autonomous Agents that Survives Rollback,
Cloning, Split-Brain and Power Loss* (Version v2). Zenodo. https://doi.org/10.5281/zenodo.24447528
(version 1: https://doi.org/10.5281/zenodo.24386392; version 2 corrects three statements of version 1).

## What this repository is

The reports of one official trial of the kernel: 13 phases (build and translation of the production code, proofs on
models and on the translated code, an independent verifier, a proven trace replay, cross-time determinism, a red-team
matrix, a Bitcoin-seeded adversarial campaign, the seal chain, and phase 12 on a Cortex-M7 microcontroller), run as an
official pair: once with the network disconnected and once online.

| Folder | Contents |
|---|---|
| `preregistration/` | The trial runner and the seal-26 manifest that committed to it **before** any run, with its OpenTimestamps proof |
| `runs/AXIOM_TRIAL_20261118T012733Z/` | Official OFFLINE run: ALL PASS |
| `runs/AXIOM_TRIAL_20261118T020914Z/` | Official ONLINE run: ALL PASS, paired with the offline run, manifest timestamped |
| `runs/AXIOM_TRIAL_20261117T182557Z/`, `…T191154Z/` | First pair, FAIL in phase 12 only (the board was reconnected before its debug probe was ready); kept as a record |
| `closure/` | Seal-27 manifest committing to all four runs and the evidence they cite, amendment E005, OpenTimestamps proof |

Each run folder holds the report (`AXIOM_REPORT.md`, `.txt`), `summary.json`, the 13 phase results and
`TRIAL_MANIFEST.txt` (SHA-256 of every file of the run).

## What is published and what is not

Published: reports, per-phase results, manifests and timestamp proofs. **Not published:** the kernel source, its
translation to Lean, the proofs, traces, firmware and raw logs. They remain in a sealed internal record; their SHA-256
values are committed in the manifests here, so they can be checked against this repository if they are released or
shown under agreement. The methods are the subject of a pending U.S. patent application.

## How to verify

```
python3 verify.py                 # integrity, Merkle roots, pairing, chain to the pre-registration (standard library only)
ots verify preregistration/SEAL26_MANIFEST.txt.ots
ots verify closure/SEAL27_MANIFEST.txt.ots
ots verify runs/AXIOM_TRIAL_20261118T020914Z/TRIAL_MANIFEST.txt.ots
```
(`ots` is the OpenTimestamps client: `pip install opentimestamps-client`.)

## What these results do not claim

They do not show that the kernel stops real attacks on deployed agents, that its geometric admission adds value over a
cumulative budget (an open, pre-registered question), or availability without a backup supply for the hardware
witness. The composition of the per-guard theorems into one refinement theorem is argued, not proved. There has been
no external audit; the adversary and the oracle share an author.

## Contact

Causal Nexus Systems LLC — Orlando, Florida, USA.
