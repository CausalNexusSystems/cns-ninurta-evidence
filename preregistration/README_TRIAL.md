# CNS AXIOM V3.4 — Trial

Thirteen phases (0-12). Each phase **re-executes** its instrument or **re-hashes** its sealed evidence in the same run; no verdict
is copied from an earlier run. Output: `trial/runs/AXIOM_TRIAL_<UTC>/` with `phaseN/phaseN_result.json`,
`AXIOM_REPORT.md`, `AXIOM_REPORT.txt`, `summary.json`, the RFC 6962 Merkle root of the thirteen phase seals and
`TRIAL_MANIFEST.txt` (stamped with OpenTimestamps when every phase passes).

| Phase | Name | What runs in this phase |
|---|---|---|
| 0 | Network & Toolchain Status | offline: every probe must fail; online: explorers reachable and the offline counterpart verified; toolchain; free disk |
| 1 | Sealed Source & Evidence Integrity | every package `EXPECTED_SHA256.txt` and every seal manifest re-hashed |
| 2 | Production Kernel | `candidate10/run_c10.sh`: tests, candidate8 ≡ candidate10 (3 witness modes × 3000 worlds), Aeneas translation, Lean compile, axiom whitelist |
| 3 | Model Proofs | `lean_f1`, `lean_f2`, `lean_f3`, `lean_f3b`, `lean_g` runners with their sabotage controls |
| 4 | Formal Proofs on the Translated Code | proof packages r4–r9 first checked identical to the sealed copies (seals 17–21 and 25), then re-proved with all controls |
| 5 | Independent Verification | `verifier_f3/run_verifier.sh` (Python, own Ed25519 RFC 8032, tamper and mutant controls) |
| 6 | Model-Code Bridge | every model-G guard and every hardware-witness fail-closed property mapped to a theorem proved in phase 4 of this run |
| 7 | ReplayG | `replay_g_v2/run_replay_g.sh`: kernel traces replayed on model G by a reproducer proved sound in Lean; 15 mutants and 2 tampered traces must be caught |
| 8 | Determinism | the sealed exporter is rebuilt and must regenerate, bit for bit, the 3000-world traces sealed in seal 13 |
| 9 | Red Team | matrix of planted faults caught across phases 3, 4, 5, 7 and 12 |
| 10 | Bitcoin-Seeded Campaign 0003 | seed block hash re-read from two explorers; campaign attested before the seed block; formal evidence re-hashed; every cohort 0 violations |
| 11 | Seal Chain | every OpenTimestamps seal verified against Bitcoin (two explorers); manifest chain from seal 16 onward |
| 12 | Silicon (MIMXRT1060-EVK, RAM only) | `silicio/kat/run_kat_placa.sh`: production kernel KAT bit-identical board = Mac = cloud; `silicio/s345/run_s345_placa.sh`: S3 core clock against the 32768 Hz RTC and cycles per operation, S4 SNVS hardware witness fail-closed (after power-up, warm reload, power cut), S5 300 ReplayG worlds generated on the board = Mac = sealed prefix and accepted by the proved reproducer; finally the board is read back in factory state |

Official pair (as in every CNS trial): an **OFFLINE** run with the network disconnected for the whole run, then an
**ONLINE** run. The online run requires its offline counterpart (ALL PASS over the same sealed source digest), re-checks
phases 10–11 against two Bitcoin explorers and stamps `TRIAL_MANIFEST.txt`, which contains `PAIR.txt` (the offline
run and the sha256 of its manifest). Offline, phases 10–11 recompute everything locally (seal digests and hash chains up
to the block-header commitment; campaign evidence and seed) and leave only the explorer look-ups to the online run.

Prerequisites: all seals closed (`close_all_seals.sh`), campaign 0003 run once, the MIMXRT1060-EVK connected by USB.
Phase 12 asks **twice** to unplug the board for 10 s with every light off (prompts appear in the terminal). Offline,
cargo runs with `CARGO_NET_OFFLINE=true`: every crate must already be in the local cache (it is, after the earlier runs).

```
bash /Volumes/CNS_SYSTEMS/AXIOM/axiom_v3_4/trial_v3/run_axiom_trial.sh offline    # network OFF
bash /Volumes/CNS_SYSTEMS/AXIOM/axiom_v3_4/trial_v3/run_axiom_trial.sh online     # network ON
```
