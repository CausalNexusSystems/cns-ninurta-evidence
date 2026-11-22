# CNS AXIOM V3.4.0 — Run Report — AXIOM_TRIAL_20261117T182557Z

> This report states only what was directly observed in this run: pass/fail outcomes, verdicts, aggregate counts and cryptographic integrity. Every phase re-executes or re-hashes its evidence in this run; nothing is copied from an earlier run.

- **Run ID:** AXIOM_TRIAL_20261117T182557Z
- **Mode:** OFFLINE (no network for the whole run)
- **Timestamp (UTC):** 2026-11-17T19:11:29Z
- **Kernel version:** 3.4.0 (existence-kernel, candidate 10 production path; candidate 8 for the sealed adversarial campaign)
- **Organization:** Causal Nexus Systems LLC — Anthony Moreno, Founder & CEO
- **Assumptions (FR-0001):** S1 CAS freshness witness · S2 Ed25519 unforgeable · S3 binding witness · S4 SHA-256 collision resistant

## Summary

| Phase | Name | Result |
|---|---|---|
| 0 | Network & Toolchain Status | ✅ PASS |
| 1 | Sealed Source & Evidence Integrity | ✅ PASS |
| 2 | Production Kernel: candidate10 Build, Equivalence & Translation | ✅ PASS |
| 3 | Model Proofs (F1, F2, F3, F3b, G) | ✅ PASS |
| 4 | Formal Proofs on the Translated Production Code | ✅ PASS |
| 5 | Independent Verification (Python, own Ed25519) | ✅ PASS |
| 6 | Model-Code Bridge (model G guards) | ✅ PASS |
| 7 | ReplayG — Code-to-Model Conformance | ✅ PASS |
| 8 | Determinism — Cross-Time Bit-Identical Replay | ✅ PASS |
| 9 | Red Team — Planted-Fault Matrix | ✅ PASS |
| 10 | Bitcoin-Seeded Adversarial Campaign 0003 | ✅ PASS |
| 11 | Seal Chain & Non-Regression (Bitcoin) | ✅ PASS |
| 12 | Silicon — MIMXRT1060-EVK, RAM only (KAT, S3, S4, S5) | ❌ FAIL |

**Overall: ❌ FAIL**

Phase Merkle root (RFC 6962): `fc267ed00b94b9bb4249b20ed98792c37d53c20749cfb10e3daf820496c951a8`

## Phase 0 — Network & Toolchain Status

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P0.1 | TCP 1.1.1.1:53 unreachable | ℹ️ INFO |
| P0.2 | TCP 8.8.8.8:53 unreachable | ℹ️ INFO |
| P0.3 | TCP blockstream.info:443 unreachable | ℹ️ INFO |
| P0.4 | TCP mempool.space:443 unreachable | ℹ️ INFO |
| P0.5 | OFFLINE run: the machine has no network for the whole run (all probes unreachable) | ✅ PASS |
| P0.6 | cargo: cargo 1.94.1 (29ea6fb6a 2026-03-24) | ✅ PASS |
| P0.7 | rustc: rustc 1.94.1 (e408947bf 2026-03-25) | ✅ PASS |
| P0.8 | python3: Python 3.13.7 | ✅ PASS |
| P0.9 | lean: Lean (version 4.20.0, x86_64-apple-darwin22.6.0, commit 77cfc4d1a4f6, Release) | ✅ PASS |
| P0.10 | probe-rs: probe-rs 0.32.0 (git commit: crates.io) | ✅ PASS |
| P0.11 | opentimestamps client: /Users/anthonymoreno/.ots-venv/bin/ots | ✅ PASS |
| P0.12 | free disk on the home volume: 11.7 GB (>= 6 GB required) | ✅ PASS |

Phase seal: `8fc3b47aecae0f1e7ef4e0f8b3bbbb05a832ce60edec921de6f80557d2c77155` — full detail in `phase0/phase0_result.json`

## Phase 1 — Sealed Source & Evidence Integrity

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P1.1 | 28 package lists (294 files) and 23 seal manifests (602 files) re-hashed | ✅ PASS |
| P1.2 | candidate: 14 files equal their sealed list | ✅ PASS |
| P1.3 | candidate10: 22 files equal their sealed list | ✅ PASS |
| P1.4 | candidate4: 14 files equal their sealed list | ✅ PASS |
| P1.5 | candidate5: 14 files equal their sealed list | ✅ PASS |
| P1.6 | candidate6: 17 files equal their sealed list | ✅ PASS |
| P1.7 | candidate7: 17 files equal their sealed list | ✅ PASS |
| P1.8 | candidate8: 18 files equal their sealed list | ✅ PASS |
| P1.9 | candidate9: 19 files equal their sealed list | ✅ PASS |
| P1.10 | candidate_finalizer: 7 files equal their sealed list | ✅ PASS |
| P1.11 | cohorts: 12 files equal their sealed list | ✅ PASS |
| P1.12 | cohorts_v2: 12 files equal their sealed list | ✅ PASS |
| P1.13 | cohorts_v3: 13 files equal their sealed list | ✅ PASS |
| P1.14 | conform_f3: 9 files equal their sealed list | ✅ PASS |
| P1.15 | conform_f3b: 9 files equal their sealed list | ✅ PASS |
| P1.16 | h8h9: 4 files equal their sealed list | ✅ PASS |
| P1.17 | h8h9_c6: 4 files equal their sealed list | ✅ PASS |
| P1.18 | h8h9_c7: 4 files equal their sealed list | ✅ PASS |
| P1.19 | h8h9_c8: 4 files equal their sealed list | ✅ PASS |
| P1.20 | lean_f1: 7 files equal their sealed list | ✅ PASS |
| P1.21 | lean_f2: 6 files equal their sealed list | ✅ PASS |
| P1.22 | lean_f3: 9 files equal their sealed list | ✅ PASS |
| P1.23 | lean_f3b: 9 files equal their sealed list | ✅ PASS |
| P1.24 | lean_g: 5 files equal their sealed list | ✅ PASS |
| P1.25 | replay_g: 13 files equal their sealed list | ✅ PASS |
| P1.26 | replay_g_v2: 13 files equal their sealed list | ✅ PASS |
| P1.27 | trial_v2: 3 files equal their sealed list | ✅ PASS |
| P1.28 | trial_v3: 3 files equal their sealed list | ✅ PASS |
| P1.29 | verifier_f3: 13 files equal their sealed list | ✅ PASS |
| P1.30 | SEAL_MANIFEST.txt: 5 sealed files unchanged | ✅ PASS |
| P1.31 | SEAL4_MANIFEST.txt: 31 sealed files unchanged | ✅ PASS |
| P1.32 | SEAL6_MANIFEST.txt: 24 sealed files unchanged | ✅ PASS |
| P1.33 | SEAL7_MANIFEST.txt: 125 sealed files unchanged | ✅ PASS |
| P1.34 | SEAL8_MANIFEST.txt: 22 sealed files unchanged | ✅ PASS |
| P1.35 | SEAL9_MANIFEST.txt: 29 sealed files unchanged | ✅ PASS |
| P1.36 | SEAL10_MANIFEST.txt: 6 sealed files unchanged | ✅ PASS |
| P1.37 | SEAL11_MANIFEST.txt: 11 sealed files unchanged | ✅ PASS |
| P1.38 | SEAL12_MANIFEST.txt: 11 sealed files unchanged | ✅ PASS |
| P1.39 | SEAL13_MANIFEST.txt: 8 sealed files unchanged | ✅ PASS |
| P1.40 | SEAL14_MANIFEST.txt: 12 sealed files unchanged | ✅ PASS |
| P1.41 | SEAL15_MANIFEST.txt: 11 sealed files unchanged | ✅ PASS |
| P1.42 | SEAL16_MANIFEST.txt: 19 sealed files unchanged | ✅ PASS |
| P1.43 | SEAL17_MANIFEST.txt: 20 sealed files unchanged | ✅ PASS |
| P1.44 | SEAL18_MANIFEST.txt: 18 sealed files unchanged | ✅ PASS |
| P1.45 | SEAL19_MANIFEST.txt: 17 sealed files unchanged | ✅ PASS |
| P1.46 | SEAL20_MANIFEST.txt: 17 sealed files unchanged | ✅ PASS |
| P1.47 | SEAL21_MANIFEST.txt: 20 sealed files unchanged | ✅ PASS |
| P1.48 | SEAL22_MANIFEST.txt: 19 sealed files unchanged | ✅ PASS |
| P1.49 | SEAL23_MANIFEST.txt: 80 sealed files unchanged | ✅ PASS |
| P1.50 | SEAL24_MANIFEST.txt: 25 sealed files unchanged | ✅ PASS |
| P1.51 | SEAL25_MANIFEST.txt: 65 sealed files unchanged | ✅ PASS |
| P1.52 | SEAL26_MANIFEST.txt: 7 sealed files unchanged | ✅ PASS |

Phase seal: `c87721e08c63f9185ae46a1081b420814a76c90d4af8b8b0b140bf87fd056d0c` — full detail in `phase1/phase1_result.json`

## Phase 2 — Production Kernel: candidate10 Build, Equivalence & Translation

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P2.1 | candidate10_pipeline (rc=0): 15 PASS, 0 FAIL; 15 evidence files re-hashed | ✅ PASS |
| P2.2 | candidate10_pipeline · PASS candidate10 coincide con su lista | ✅ PASS |
| P2.3 | candidate10_pipeline · PASS candidate8 intacto | ✅ PASS |
| P2.4 | candidate10_pipeline · PASS candidate9 intacto | ✅ PASS |
| P2.5 | candidate10_pipeline · PASS verifier_f3 intacto | ✅ PASS |
| P2.6 | candidate10_pipeline · PASS lean_f3b intacto | ✅ PASS |
| P2.7 | candidate10_pipeline · PASS 129 pruebas + 13 doctests | ✅ PASS |
| P2.8 | candidate10_pipeline · PASS el harness compila sin cambios | ✅ PASS |
| P2.9 | candidate10_pipeline · PASS modulos de prueba: candidate8=8 candidate10=8 identicos=True | ✅ PASS |
| P2.10 | candidate10_pipeline · PASS testigo=strict: trazas identicas (c51c758b0986647e5f5fa72e3cbd3a1f40be654b20b9062a23190ec51d9f52ae) y anclas/firmas/compromisos identicos (2418a4efa7b4ebc9 3000) | ✅ PASS |
| P2.11 | candidate10_pipeline · PASS testigo=number: trazas identicas (c51c758b0986647e5f5fa72e3cbd3a1f40be654b20b9062a23190ec51d9f52ae) y anclas/firmas/compromisos identicos (2418a4efa7b4ebc9 3000) | ✅ PASS |
| P2.12 | candidate10_pipeline · PASS testigo=nonstrict: trazas identicas (b7fb384a226b0bbd5a952c3d1e93c9214ad12d9e1fc4f13334e161cda30e3b40) y anclas/firmas/compromisos identicos (49cfa47d181ddcd8 3000) | ✅ PASS |
| P2.13 | candidate10_pipeline · PASS control: una firma alterada cambia el resumen canonico | ✅ PASS |
| P2.14 | candidate10_pipeline · VERIFICADOR INDEPENDIENTE: PASS | ✅ PASS |
| P2.15 | candidate10_pipeline · REPLAY F3b: PASS (toda transicion del Rust fue una transicion del modelo demostrado) | ✅ PASS |
| P2.16 | candidate10_pipeline · PASS axiomas: todos en la lista permitida (S2/S4 + logica estandar) | ✅ PASS |

Phase seal: `3f0326a92319bc048acf9965769e7f2fa1b133b860b8a843772307fac58f073f` — full detail in `phase2/phase2_result.json`

## Phase 3 — Model Proofs (F1, F2, F3, F3b, G)

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P3.1 | lean_f1 (rc=0): 10 PASS, 0 FAIL; 4 evidence files re-hashed | ✅ PASS |
| P3.2 | lean_f1 · PASS lean_f1 coincide con su lista | ✅ PASS |
| P3.3 | lean_f1 · PASS compila sin errores | ✅ PASS |
| P3.4 | lean_f1 · PASS sin sorry | ✅ PASS |
| P3.5 | lean_f1 · PASS axiomas: solo propext y Quot.sound (o ninguno) | ✅ PASS |
| P3.6 | lean_f1 · PASS sabotaje S1_sin_consumo_unico (errores=1, esperado break) | ✅ PASS |
| P3.7 | lean_f1 · PASS sabotaje S2_consume_tras_colapso (errores=2, esperado break) | ✅ PASS |
| P3.8 | lean_f1 · PASS sabotaje S3_cand7_declarado_seguro (errores=1, esperado break) | ✅ PASS |
| P3.9 | lean_f1 · PASS sabotaje S4_efecto_sin_testigo (errores=4, esperado break) | ✅ PASS |
| P3.10 | lean_f1 · PASS sabotaje S5_control_sin_cambio (errores=0, esperado ok) | ✅ PASS |
| P3.11 | lean_f1 · LEAN F1: PASS | ✅ PASS |
| P3.12 | lean_f2 (rc=0): 12 PASS, 0 FAIL; 4 evidence files re-hashed | ✅ PASS |
| P3.13 | lean_f2 · PASS lean_f2 coincide con su lista | ✅ PASS |
| P3.14 | lean_f2 · PASS compila sin errores | ✅ PASS |
| P3.15 | lean_f2 · PASS sin sorry | ✅ PASS |
| P3.16 | lean_f2 · PASS axiomas: solo propext y Quot.sound (o ninguno) | ✅ PASS |
| P3.17 | lean_f2 · PASS sabotaje S1_sin_consumo_unico (errores=1, esperado break) | ✅ PASS |
| P3.18 | lean_f2 · PASS sabotaje S2_consume_tras_colapso (errores=2, esperado break) | ✅ PASS |
| P3.19 | lean_f2 · PASS sabotaje S3_cand7_declarado_seguro (errores=1, esperado break) | ✅ PASS |
| P3.20 | lean_f2 · PASS sabotaje S4_efecto_sin_testigo (errores=4, esperado break) | ✅ PASS |
| P3.21 | lean_f2 · PASS sabotaje S6_testigo_estricto_no_rompe (errores=2, esperado break) | ✅ PASS |
| P3.22 | lean_f2 · PASS sabotaje S7_regla_un_consumo_no_rompe (errores=2, esperado break) | ✅ PASS |
| P3.23 | lean_f2 · PASS sabotaje S5_control_sin_cambio (errores=0, esperado ok) | ✅ PASS |
| P3.24 | lean_f2 · LEAN F2: PASS | ✅ PASS |
| P3.25 | lean_f3 (rc=0): 14 PASS, 0 FAIL; 8 evidence files re-hashed | ✅ PASS |
| P3.26 | lean_f3 · PASS lean_f3 y conform_f3 coinciden con sus listas | ✅ PASS |
| P3.27 | lean_f3 · PASS candidate8 intacto | ✅ PASS |
| P3.28 | lean_f3 · PASS modelo F3 compila (sin sorry: 0 avisos) | ✅ PASS |
| P3.29 | lean_f3 · PASS axiomas: solo propext y Quot.sound | ✅ PASS |
| P3.30 | lean_f3 · PASS sabotaje S8_reproductor_acepta_aperturas_ilegales (errores=1) | ✅ PASS |
| P3.31 | lean_f3 · PASS sabotaje S9_reproductor_acepta_testigo_ilegal (errores=1) | ✅ PASS |
| P3.32 | lean_f3 · PASS sabotaje S5_control (errores=0) | ✅ PASS |
| P3.33 | lean_f3 · PASS generador compila | ✅ PASS |
| P3.34 | lean_f3 · REPLAY F3: PASS (toda transicion del Rust fue una transicion del modelo demostrado) | ✅ PASS |
| P3.35 | lean_f3 · PASS M05 rechazado por el reproductor | ✅ PASS |
| P3.36 | lean_f3 · PASS M14 rechazado por el reproductor | ✅ PASS |
| P3.37 | lean_f3 · PASS M20 rechazado por el reproductor | ✅ PASS |
| P3.38 | lean_f3 · PASS MW rechazado por el reproductor | ✅ PASS |
| P3.39 | lean_f3 · F3 (inclusion de trazas): PASS | ✅ PASS |
| P3.40 | lean_f3b (rc=0): 16 PASS, 0 FAIL; 8 evidence files re-hashed | ✅ PASS |
| P3.41 | lean_f3b · PASS lean_f3 y conform_f3 coinciden con sus listas | ✅ PASS |
| P3.42 | lean_f3b · PASS candidate8 intacto | ✅ PASS |
| P3.43 | lean_f3b · PASS modelo F3 compila (sin sorry: 0 avisos) | ✅ PASS |
| P3.44 | lean_f3b · PASS axiomas: solo propext y Quot.sound | ✅ PASS |
| P3.45 | lean_f3b · PASS sabotaje S8_reproductor_acepta_aperturas_ilegales (errores=1) | ✅ PASS |
| P3.46 | lean_f3b · PASS sabotaje S9_reproductor_acepta_testigo_ilegal (errores=1) | ✅ PASS |
| P3.47 | lean_f3b · PASS sabotaje S10_linaje_solo_por_indice (errores=2) | ✅ PASS |
| P3.48 | lean_f3b · PASS sabotaje S5_control (errores=0) | ✅ PASS |
| P3.49 | lean_f3b · PASS generador compila | ✅ PASS |
| P3.50 | lean_f3b · REPLAY F3b: PASS (toda transicion del Rust fue una transicion del modelo demostrado) | ✅ PASS |
| P3.51 | lean_f3b · PASS M05 rechazado por el reproductor | ✅ PASS |
| P3.52 | lean_f3b · PASS M14 rechazado por el reproductor | ✅ PASS |
| P3.53 | lean_f3b · PASS M15 rechazado por el reproductor | ✅ PASS |
| P3.54 | lean_f3b · PASS M20 rechazado por el reproductor | ✅ PASS |
| P3.55 | lean_f3b · PASS MW rechazado por el reproductor | ✅ PASS |
| P3.56 | lean_f3b · F3b (inclusion de trazas con ramas): PASS | ✅ PASS |
| P3.57 | lean_g (rc=0): 10 PASS, 0 FAIL; 10 evidence files re-hashed | ✅ PASS |
| P3.58 | lean_g · PASS lean_g coincide con su lista | ✅ PASS |
| P3.59 | lean_g · PASS modelo G compila (avisos sorry: 0) | ✅ PASS |
| P3.60 | lean_g · PASS axiomas: 15 teoremas, solo propext y Quot.sound | ✅ PASS |
| P3.61 | lean_g · PASS sabotaje G1_open_sin_verificar_firma (errores=4) | ✅ PASS |
| P3.62 | lean_g · PASS sabotaje G2_contador_no_estricto (errores=1) | ✅ PASS |
| P3.63 | lean_g · PASS sabotaje G3_recibo_perdido_no_envenena (errores=2) | ✅ PASS |
| P3.64 | lean_g · PASS sabotaje G4_ancla_inyectada_pasa_por_firmada (errores=2) | ✅ PASS |
| P3.65 | lean_g · PASS sabotaje G5_envenenado_puede_consumir (errores=1) | ✅ PASS |
| P3.66 | lean_g · PASS sabotaje G0_control (errores=0) | ✅ PASS |
| P3.67 | lean_g · MODELO G (firmas, contadores, compuerta de efectos): PASS | ✅ PASS |

Phase seal: `4202eb4c4cb831012c70f9ab78fccf0df8ad7cdbb13c68abb7b8f55c8bb05a32` — full detail in `phase3/phase3_result.json`

## Phase 4 — Formal Proofs on the Translated Production Code

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P4.1 | pruebas_r4 (rc=0): 19 PASS, 0 FAIL; 18 evidence files re-hashed | ✅ PASS |
| P4.2 | pruebas_r4 · PASS archivos de la ronda coinciden con su lista | ✅ PASS |
| P4.3 | pruebas_r4 · PASS Types.lean = sellado (sello 16) | ✅ PASS |
| P4.4 | pruebas_r4 · PASS Funs.lean = sellado (sello 16) | ✅ PASS |
| P4.5 | pruebas_r4 · PASS TypesExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.6 | pruebas_r4 · PASS FunsExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.7 | pruebas_r4 · PASS proyecto compilado | ✅ PASS |
| P4.8 | pruebas_r4 · DEMOSTRADO M0_sin_cabeza_solo_paso_1 (36s), axiomas en lista blanca | ✅ PASS |
| P4.9 | pruebas_r4 · DEMOSTRADO T1_no_autoriza_paso_consumido (26s), axiomas en lista blanca | ✅ PASS |
| P4.10 | pruebas_r4 · DEMOSTRADO T3_no_autoriza_tras_colapso (15s), axiomas en lista blanca | ✅ PASS |
| P4.11 | pruebas_r4 · PASS N1_sin_hipotesis falla como debe (objetivo sin resolver) | ✅ PASS |
| P4.12 | pruebas_r4 · PASS N2_paso_no_consumido falla como debe (objetivo sin resolver) | ✅ PASS |
| P4.13 | pruebas_r4 · PASS N3_mutante_sin_step_consumed falla como debe (objetivo sin resolver) | ✅ PASS |
| P4.14 | pruebas_r4 · PASS N4_mutante_sin_colapso falla como debe (objetivo sin resolver) | ✅ PASS |
| P4.15 | pruebas_r4 · PASS N5_con_cabeza_de_linaje falla como debe (objetivo sin resolver) | ✅ PASS |
| P4.16 | pruebas_r4 · PASS N3_mutante_sin_step_consumed: lo que queda abierto es el camino que AUTORIZA | ✅ PASS |
| P4.17 | pruebas_r4 · PASS N4_mutante_sin_colapso: lo que queda abierto es el camino que AUTORIZA | ✅ PASS |
| P4.18 | pruebas_r4 · PASS N1_sin_hipotesis: lo que queda abierto es el camino que AUTORIZA | ✅ PASS |
| P4.19 | pruebas_r4 · PASS N5: lo que queda abierto es 'paso = 1' | ✅ PASS |
| P4.20 | pruebas_r4 · TEOREMAS SOBRE EL CODIGO TRADUCIDO (T1, T3, M0) + 5 CONTROLES: PASS | ✅ PASS |
| P4.21 | pruebas_r5 (rc=0): 13 PASS, 0 FAIL; 15 evidence files re-hashed | ✅ PASS |
| P4.22 | pruebas_r5 · PASS archivos de la ronda coinciden con su lista | ✅ PASS |
| P4.23 | pruebas_r5 · PASS Types.lean = sellado (sello 16) | ✅ PASS |
| P4.24 | pruebas_r5 · PASS Funs.lean = sellado (sello 16) | ✅ PASS |
| P4.25 | pruebas_r5 · PASS TypesExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.26 | pruebas_r5 · PASS FunsExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.27 | pruebas_r5 · PASS proyecto compilado | ✅ PASS |
| P4.28 | pruebas_r5 · DEMOSTRADO R5_FR12_sobre_codigo_traducido (28s), axiomas en lista blanca | ✅ PASS |
| P4.29 | pruebas_r5 · PASS C1_sin_hipotesis: lo abierto son exactamente los 2 caminos de autorizacion real (commit_consume Ok) | ✅ PASS |
| P4.30 | pruebas_r5 · PASS C2_mutante_sin_step_consumed: lo abierto son exactamente los 2 caminos de autorizacion real (commit_consume Ok) | ✅ PASS |
| P4.31 | pruebas_r5 · PASS C3_mutante_sin_colapso: lo abierto son exactamente los 2 caminos de autorizacion real (commit_consume Ok) | ✅ PASS |
| P4.32 | pruebas_r5 · PASS C4: sin el registro, la prueba se traba justo en el push de consumed_heads | ✅ PASS |
| P4.33 | pruebas_r5 · PASS C5: lo registrado es el hash causal, no el previo | ✅ PASS |
| P4.34 | pruebas_r5 · FR-1.2 SOBRE EL CODIGO TRADUCIDO (T2 + FR12) + 5 CONTROLES: PASS | ✅ PASS |
| P4.35 | pruebas_r6 (rc=0): 13 PASS, 0 FAIL; 15 evidence files re-hashed | ✅ PASS |
| P4.36 | pruebas_r6 · PASS archivos de la ronda coinciden con su lista | ✅ PASS |
| P4.37 | pruebas_r6 · PASS Types.lean = sellado (sello 16) | ✅ PASS |
| P4.38 | pruebas_r6 · PASS Funs.lean = sellado (sello 16) | ✅ PASS |
| P4.39 | pruebas_r6 · PASS TypesExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.40 | pruebas_r6 · PASS FunsExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.41 | pruebas_r6 · PASS proyecto compilado | ✅ PASS |
| P4.42 | pruebas_r6 · DEMOSTRADO R6_FR11_sobre_codigo_traducido (27s), axiomas en lista blanca | ✅ PASS |
| P4.43 | pruebas_r6 · PASS C6_mutante_denegado_ejecuta: si la autoridad DENIEGA y aun asi se llama al ejecutor, queda abierto exactamente ex1 = ex | ✅ PASS |
| P4.44 | pruebas_r6 · PASS C7_mutante_envenenado_ejecuta: con la compuerta envenenada y llamada al ejecutor, queda abierto exactamente ex1 = ex | ✅ PASS |
| P4.45 | pruebas_r6 · PASS C8_sin_efecto_previo: sin efecto previo (recibo Denied) el corolario no se sostiene | ✅ PASS |
| P4.46 | pruebas_r6 · PASS C9_otro_paso_causal: con otro paso causal no hay exclusion (queda abierto adm2.causal_hash = adm.causal_hash) | ✅ PASS |
| P4.47 | pruebas_r6 · PASS C10_mutante_recibo: si el recibo no registra el resultado real, L_rcpt se traba en la rama Err | ✅ PASS |
| P4.48 | pruebas_r6 · FR-1.1 SOBRE EL CODIGO TRADUCIDO (FR11 + un efecto por paso) + 5 CONTROLES: PASS | ✅ PASS |
| P4.49 | pruebas_r7 (rc=0): 13 PASS, 0 FAIL; 15 evidence files re-hashed | ✅ PASS |
| P4.50 | pruebas_r7 · PASS archivos de la ronda coinciden con su lista | ✅ PASS |
| P4.51 | pruebas_r7 · PASS Types.lean = sellado (sello 16) | ✅ PASS |
| P4.52 | pruebas_r7 · PASS Funs.lean = sellado (sello 16) | ✅ PASS |
| P4.53 | pruebas_r7 · PASS TypesExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.54 | pruebas_r7 · PASS FunsExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.55 | pruebas_r7 · PASS proyecto compilado | ✅ PASS |
| P4.56 | pruebas_r7 · DEMOSTRADO R7_F45_open_typed_sobre_codigo_traducido (28s), axiomas en lista blanca | ✅ PASS |
| P4.57 | pruebas_r7 · PASS C11_mutante_salto_dos: si la ligadura aceptara seq+2, queda abierto exactamente sat(wseq,2) = sat(wseq,1) | ✅ PASS |
| P4.58 | pruebas_r7 · PASS C12_mutante_sin_firma: sin verificar la firma, queda abierto exactamente verify_signature = ok true | ✅ PASS |
| P4.59 | pruebas_r7 · PASS C13_mutante_sin_rollback: sin el chequeo de rollback, queda abierto exactamente fl <= val.seq | ✅ PASS |
| P4.60 | pruebas_r7 · PASS C14_mutante_sin_avance: si nunca avanza el testigo, queda abierto exactamente el roll-forward | ✅ PASS |
| P4.61 | pruebas_r7 · PASS C15_sin_supuesto_S3: sin admitir el testigo no vinculante (S3), queda abierto False con binds = false | ✅ PASS |
| P4.62 | pruebas_r7 · F4/F5 SOBRE open_typed EN EL CODIGO TRADUCIDO + 5 CONTROLES: PASS | ✅ PASS |
| P4.63 | pruebas_r8 (rc=0): 14 PASS, 0 FAIL; 18 evidence files re-hashed | ✅ PASS |
| P4.64 | pruebas_r8 · PASS archivos de la ronda coinciden con su lista | ✅ PASS |
| P4.65 | pruebas_r8 · PASS Types.lean = sellado (sello 16) | ✅ PASS |
| P4.66 | pruebas_r8 · PASS Funs.lean = sellado (sello 16) | ✅ PASS |
| P4.67 | pruebas_r8 · PASS TypesExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.68 | pruebas_r8 · PASS FunsExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.69 | pruebas_r8 · PASS proyecto compilado | ✅ PASS |
| P4.70 | pruebas_r8 · DEMOSTRADO R8_puente_G_sobre_codigo_traducido (29s), axiomas en lista blanca | ✅ PASS |
| P4.71 | pruebas_r8 · PASS C16_sin_hipotesis_contador: sin la hipotesis de contador queda abierto exactamente el camino real con contador mayor | ✅ PASS |
| P4.72 | pruebas_r8 · PASS C17_mutante_contador_igual: si se aceptara contador igual al ultimo, queda abierto ese replay (counter <= last y no <) | ✅ PASS |
| P4.73 | pruebas_r8 · PASS C18_mutante_ignora_almacen: si se ignora el fallo del almacen, queda abierto exactamente commit = Ok | ✅ PASS |
| P4.74 | pruebas_r8 · PASS C19_mutante_no_envenena: si un recibo no anclado no envenena, queda abierta la existencia del ancla | ✅ PASS |
| P4.75 | pruebas_r8 · PASS C20_mutante_envenenada_consume: si la compuerta envenenada consume, queda abierto exactamente ag1 = ag | ✅ PASS |
| P4.76 | pruebas_r8 · PASS C21_sin_contador_cero: sin h0 quedan abiertos exactamente los 2 caminos reales de autorizacion | ✅ PASS |
| P4.77 | pruebas_r8 · PUENTE G EN EL CODIGO TRADUCIDO (G1,G2,G3) + 6 CONTROLES: PASS | ✅ PASS |
| P4.78 | pruebas_r9 (rc=0): 11 PASS, 0 FAIL; 11 evidence files re-hashed | ✅ PASS |
| P4.79 | pruebas_r9 · PASS archivos de la ronda coinciden con su lista | ✅ PASS |
| P4.80 | pruebas_r9 · PASS Types.lean = sellado (sello 16) | ✅ PASS |
| P4.81 | pruebas_r9 · PASS Funs.lean = sellado (sello 16) | ✅ PASS |
| P4.82 | pruebas_r9 · PASS TypesExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.83 | pruebas_r9 · PASS FunsExternal.lean = sellado (sello 16) | ✅ PASS |
| P4.84 | pruebas_r9 · PASS proyecto compilado | ✅ PASS |
| P4.85 | pruebas_r9 · DEMOSTRADO R9_fail_closed_testigo_perdido (31s), axiomas en lista blanca | ✅ PASS |
| P4.86 | pruebas_r9 · PASS C22_floor_uno: con floor 1 queda abierto exactamente el sucesor del ancla fresca (seq = 0+1, roll-forward) | ✅ PASS |
| P4.87 | pruebas_r9 · PASS C23_sin_binds: sin binds = true queda abierto exactamente el testigo que no liga (binds = false) | ✅ PASS |
| P4.88 | pruebas_r9 · PASS C24_floor_cero: con floor 0 queda abierto exactamente el genesis sobre testigo fresco (floor == 0) | ✅ PASS |
| P4.89 | pruebas_r9 · R9 FAIL-CLOSED CON TESTIGO PERDIDO (4 teoremas + no vacuidad) + 3 CONTROLES: PASS | ✅ PASS |

Phase seal: `510723dbb0706d04661a23885c29f53bf1af6285f26d239474e94e79572112fe` — full detail in `phase4/phase4_result.json`

## Phase 5 — Independent Verification (Python, own Ed25519)

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P5.1 | verifier_f3 (rc=0): 13 PASS, 0 FAIL; 6 evidence files re-hashed | ✅ PASS |
| P5.2 | verifier_f3 · PASS verifier_f3 coincide con su lista | ✅ PASS |
| P5.3 | verifier_f3 · PASS candidate8 intacto | ✅ PASS |
| P5.4 | verifier_f3 · PASS Ed25519 propio contra el vector de prueba 1 de RFC 8032 (y rechazo del mensaje alterado) | ✅ PASS |
| P5.5 | verifier_f3 · PASS exportador compila | ✅ PASS |
| P5.6 | verifier_f3 · VERIFICADOR INDEPENDIENTE: PASS | ✅ PASS |
| P5.7 | verifier_f3 · PASS la misma corrida tambien pasa el reproductor Lean F3b (dos oraculos independientes) | ✅ PASS |
| P5.8 | verifier_f3 · PASS M05 detectado por el verificador | ✅ PASS |
| P5.9 | verifier_f3 · PASS M06 detectado por el verificador | ✅ PASS |
| P5.10 | verifier_f3 · PASS M10 detectado por el verificador | ✅ PASS |
| P5.11 | verifier_f3 · PASS M14 detectado por el verificador | ✅ PASS |
| P5.12 | verifier_f3 · PASS M19 detectado por el verificador | ✅ PASS |
| P5.13 | verifier_f3 · PASS MW detectado por el verificador | ✅ PASS |
| P5.14 | verifier_f3 · VERIFICADOR INDEPENDIENTE F3: PASS | ✅ PASS |

Phase seal: `0a1c63a475240d3c88584455af875c5f51b59d2239f7fe80a2be986a9a45cb29` — full detail in `phase5/phase5_result.json`

## Phase 6 — Model-Code Bridge (model G guards)

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P6.1 | G guard [openp.hsig signature check] <- `F45_apertura` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.2 | G guard [openp.hacc binding to witness] <- `F4_ligadura` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.3 | G guard [openp.hacc binding to witness] <- `F45_apertura_ligada` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.4 | G guard [successor is +1] <- `F4_sucesor_es_mas_uno` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.5 | G guard [commit ws=ww=true] <- `G2_commit_exige_almacen_y_testigo` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.6 | G guard [Valid: collapse not in h] <- `T3_no_autoriza_tras_colapso` proved in this run (T3_no_autoriza_tras_colapso.lean) | ✅ PASS |
| P6.7 | G guard [Valid: t not consumed] <- `T1_no_autoriza_paso_consumido` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.8 | G guard [Valid: t not consumed] <- `T2_autorizar_registra_el_consumo` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.9 | G guard [Valid: t not consumed] <- `FR12_no_dos_autorizaciones_del_mismo_paso` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.10 | G guard [Valid: lineage (no head)] <- `M0_lineage_ok_sin_cabeza_exige_paso_1` proved in this run (M0_sin_cabeza_solo_paso_1.lean) | ✅ PASS |
| P6.11 | G guard [CtrOK counter 0] <- `G1a_contador_cero` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.12 | G guard [CtrOK monotone] <- `G1b_contador_no_creciente` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.13 | G guard [hpois] <- `G3b_envenenada_no_consume` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.14 | G guard [hpois] <- `FR11_ejecutor_solo_tras_autorizacion` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.15 | G guard [pois := pois // !rok] <- `G3_recibo_no_anclado_envenena` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.16 | G guard [one effect per step] <- `FR11_un_efecto_por_paso` proved in this run (R8_puente_G_sobre_codigo_traducido.lean) | ✅ PASS |
| P6.17 | G guard [hardware witness lost (PGD) => authority gate never opens] <- `S4_fc_open_autoridad` proved in this run (R9_fail_closed_testigo_perdido.lean) | ✅ PASS |
| P6.18 | G guard [hardware witness lost (PGD) => effect gate never opens] <- `S4_fc_open_efectos` proved in this run (R9_fail_closed_testigo_perdido.lean) | ✅ PASS |
| P6.19 | G guard [hardware witness lost (PGD) => no authority genesis] <- `S4_fc_genesis_autoridad` proved in this run (R9_fail_closed_testigo_perdido.lean) | ✅ PASS |
| P6.20 | G guard [hardware witness lost (PGD) => no effect genesis] <- `S4_fc_genesis_efectos` proved in this run (R9_fail_closed_testigo_perdido.lean) | ✅ PASS |
| P6.21 | Composition 'all guards proved => code refines G => fr1_g holds for the code' is ARGUED, not mechanized as one theorem; its empirical evidence is phase 7 (ReplayG). | ℹ️ INFO |

Phase seal: `76d8db97fa4fc7b25d51292cc5c8875285717cc280ce29d845278a65eb2ae006` — full detail in `phase6/phase6_result.json`

## Phase 7 — ReplayG — Code-to-Model Conformance

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P7.1 | replay_g_v2 (rc=0): 27 PASS, 0 FAIL; 11 evidence files re-hashed | ✅ PASS |
| P7.2 | replay_g_v2 · PASS replay_g_v2 coincide con su lista | ✅ PASS |
| P7.3 | replay_g_v2 · PASS lean_g coincide con su lista | ✅ PASS |
| P7.4 | replay_g_v2 · PASS candidate8 coincide con su lista | ✅ PASS |
| P7.5 | replay_g_v2 · PASS verifier_f3 coincide con su lista | ✅ PASS |
| P7.6 | replay_g_v2 · PASS modelo G + ReplayGCore compilan | ✅ PASS |
| P7.7 | replay_g_v2 · PASS applyG_sound, replayG_sound, replayG_fr1: solo propext y Quot.sound | ✅ PASS |
| P7.8 | replay_g_v2 · PASS exportador compila contra candidate8 | ✅ PASS |
| P7.9 | replay_g_v2 · PASS determinismo: dos exportaciones identicas (0bac85a3034e1b68...) | ✅ PASS |
| P7.10 | replay_g_v2 · REPLAY G: PASS (toda transicion del Rust fue un Step del modelo G demostrado) | ✅ PASS |
| P7.11 | replay_g_v2 · PASS traza manipulada (ctr) rechazada | ✅ PASS |
| P7.12 | replay_g_v2 · PASS traza manipulada (eff) rechazada | ✅ PASS |
| P7.13 | replay_g_v2 · PASS M01 detectado: linea 10988: DIVERGENCIA: commit 0: el Rust firmo una operacion invalida para G (linaje/contador) REPLAY G: FA | ✅ PASS |
| P7.14 | replay_g_v2 · PASS M02 detectado: linea 376: DIVERGENCIA: testigo Rust=a0 modelo=c0@1,a0 REPLAY G: FAIL | ✅ PASS |
| P7.15 | replay_g_v2 · PASS M03 detectado: linea 49: DIVERGENCIA: open 1 2: G NO permite esta apertura REPLAY G: FAIL | ✅ PASS |
| P7.16 | replay_g_v2 · PASS M05 detectado: linea 130: DIVERGENCIA: commit 2: el Rust firmo una operacion invalida para G (linaje/contador) REPLAY G: FAIL | ✅ PASS |
| P7.17 | replay_g_v2 · PASS M06 detectado: linea 198: DIVERGENCIA: commit 0: el Rust firmo una operacion invalida para G (linaje/contador) REPLAY G: FAIL | ✅ PASS |
| P7.18 | replay_g_v2 · PASS M07 detectado: linea 118: DIVERGENCIA: open 0 0: el Rust abrio sobre un ancla con firma invalida REPLAY G: FAIL | ✅ PASS |
| P7.19 | replay_g_v2 · PASS M09 detectado: linea 570: DIVERGENCIA: commit 1: el Rust firmo una operacion invalida para G (linaje/contador) REPLAY G: FAIL | ✅ PASS |
| P7.20 | replay_g_v2 · PASS M10 detectado: linea 1184: DIVERGENCIA: commit 2: el almacen del Rust tomo un ancla que no extiende la cabeza REPLAY G: FAIL | ✅ PASS |
| P7.21 | replay_g_v2 · PASS M11 detectado: linea 2724: DIVERGENCIA: commit 1: el Rust consumio con la compuerta de efectos envenenada REPLAY G: FAIL | ✅ PASS |
| P7.22 | replay_g_v2 · PASS M14 detectado: linea 2386: DIVERGENCIA: commit 1: el Rust firmo una operacion invalida para G (linaje/contador) REPLAY G: FAI | ✅ PASS |
| P7.23 | replay_g_v2 · PASS M15 detectado: linea 214: DIVERGENCIA: commit 0: el Rust firmo una operacion invalida para G (linaje/contador) REPLAY G: FAIL | ✅ PASS |
| P7.24 | replay_g_v2 · PASS M17 detectado: efectos=0 recibos_no_anclados=0 anclas_inyectadas=455 colapsos=1911 REPLAY G: FAIL (corrida vacua: no ejercita | ✅ PASS |
| P7.25 | replay_g_v2 · PASS M18 detectado: linea 130: DIVERGENCIA: commit 2: el Rust firmo una operacion invalida para G (linaje/contador) REPLAY G: FAIL | ✅ PASS |
| P7.26 | replay_g_v2 · PASS M19 detectado: linea 300: DIVERGENCIA: testigo Rust=a000,c00@2,a00,c0@1,a0 modelo=c000@3,a000,c00@2,a00,c0@1,a0 REPLAY G: FAI | ✅ PASS |
| P7.27 | replay_g_v2 · PASS M20 detectado: linea 376: DIVERGENCIA: testigo Rust=a0 modelo=c0@1,a0 REPLAY G: FAIL | ✅ PASS |
| P7.28 | replay_g_v2 · INFO M04 fuera de alcance de G (lo cubren las cohortes), no detectado: esperado | ℹ️ INFO |
| P7.29 | replay_g_v2 · INFO M08 fuera de alcance de G (lo cubren las cohortes), no detectado: esperado | ℹ️ INFO |
| P7.30 | replay_g_v2 · INFO M12 fuera de alcance de G (lo cubren las cohortes), no detectado: esperado | ℹ️ INFO |
| P7.31 | replay_g_v2 · INFO M13 fuera de alcance de G (lo cubren las cohortes), no detectado: esperado | ℹ️ INFO |
| P7.32 | replay_g_v2 · REPLAY G (formal): PASS | ✅ PASS |

Phase seal: `4df93e82d9a32ea5b3911bc7f50d9b691439d6bd2948e55132d576adee3fc21a` — full detail in `phase7/phase7_result.json`

## Phase 8 — Determinism — Cross-Time Bit-Identical Replay

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P8.1 | determinism (rc=0): 4 PASS, 0 FAIL; 1 evidence files re-hashed | ✅ PASS |
| P8.2 | determinism · PASS sealed reference traces (seal 13) intact: evidence/verifier_f3_20261111T022103Z/traces.txt.gz | ✅ PASS |
| P8.3 | determinism · PASS sealed exporter rebuilt from source | ✅ PASS |
| P8.4 | determinism · PASS 3000 adversarial worlds regenerated now are BIT-IDENTICAL to the traces sealed in seal 13 (sha256 c51c758b0986647e5f5fa72e3cbd3a1f40be654b20b9062a23190ec51d9f52ae) | ✅ PASS |
| P8.5 | determinism · DETERMINISM: PASS | ✅ PASS |

Phase seal: `c009d96995eda6412683375a241a0942c99dd0bfdc9dd2dbe88a80bb97ea3982` — full detail in `phase8/phase8_result.json`

## Phase 9 — Red Team — Planted-Fault Matrix

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P9.1 | 80 planted faults/controls caught across 5 independent instruments; none escaped (an escape fails its own phase) | ✅ PASS |
| P9.2 | model sabotage: 32 planted faults/controls caught (phase 3) | ✅ PASS |
| P9.3 | proof controls (mutants / missing hypotheses): 23 planted faults/controls caught (phase 4) | ✅ PASS |
| P9.4 | independent verifier mutants: 7 planted faults/controls caught (phase 5) | ✅ PASS |
| P9.5 | ReplayG mutants and tampered traces: 17 planted faults/controls caught (phase 7) | ✅ PASS |
| P9.6 | silicon: tampered board trace rejected: 1 planted faults/controls caught (phase 12) | ✅ PASS |

Phase seal: `dfe6ff03c18cc8b3e4900564cca4289dd00c29a1686ae9709ac8159ec791c021` — full detail in `phase9/phase9_result.json`

## Phase 10 — Bitcoin-Seeded Adversarial Campaign 0003

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P10.1 | OFFLINE: seed block 975508 hash 0000000000000000... is re-read from two Bitcoin explorers by the ONLINE run of the pair | ℹ️ INFO |
| P10.2 | campaign definition attested in Bitcoin at block 975368 BEFORE the seed block 975508 (no seed grinding) | ✅ PASS |
| P10.3 | evidence/cohorts_v3_formal_20261113T034852Z: 125 evidence files intact | ✅ PASS |
| P10.4 | formal verdict PASS and the run used the saved block hash as seed | ✅ PASS |
| P10.5 | cohort N1: 1000 instances, 0 violations, 95% upper bound 0.00299125 | ✅ PASS |
| P10.6 | cohort N2: 1000 instances, 0 violations, 95% upper bound 0.00299125 | ✅ PASS |
| P10.7 | cohort N3: 1000 instances, 0 violations, 95% upper bound 0.00299125 | ✅ PASS |
| P10.8 | cohort N4: 1000 instances, 0 violations, 95% upper bound 0.00299125 | ✅ PASS |
| P10.9 | cohort N5: 841 instances, 0 violations, 95% upper bound 0.003555771 | ✅ PASS |
| P10.10 | cohort N6: 1000 instances, 0 violations, 95% upper bound 0.00299125 | ✅ PASS |
| P10.11 | cohort N7: 1000 instances, 0 violations, 95% upper bound 0.00299125 | ✅ PASS |
| P10.12 | cohort N8: 5000000 instances, 0 violations, 95% upper bound 5.991463e-07 | ✅ PASS |

Phase seal: `c084579962c6731d09e7257e3a2f70d052a60dd7f29e8bfb934c663a12fbe464` — full detail in `phase10/phase10_result.json`

## Phase 11 — Seal Chain & Non-Regression (Bitcoin)

Result: ✅ PASS

| Case | Check | Result |
|---|---|---|
| P11.1 | 57/57 OpenTimestamps seals: sealed digest = current digest and the hash chain up to the Bitcoin block header commitment recomputed locally; explorer check by the ONLINE run of the pair | ✅ PASS |
| P11.2 | chain: SEAL17 contains the hash of SEAL16 | ✅ PASS |
| P11.3 | chain: SEAL18 contains the hash of SEAL17 | ✅ PASS |
| P11.4 | chain: SEAL19 contains the hash of SEAL18 | ✅ PASS |
| P11.5 | chain: SEAL20 contains the hash of SEAL19 | ✅ PASS |
| P11.6 | chain: SEAL21 contains the hash of SEAL20 | ✅ PASS |
| P11.7 | chain: SEAL22 contains the hash of SEAL21 | ✅ PASS |
| P11.8 | chain: SEAL23 contains the hash of SEAL22 | ✅ PASS |
| P11.9 | chain: SEAL24 contains the hash of SEAL23 | ✅ PASS |
| P11.10 | chain: SEAL25 contains the hash of SEAL24 | ✅ PASS |
| P11.11 | chain: SEAL26 contains the hash of SEAL25 | ✅ PASS |

Phase seal: `4d27d8d21f5d322ba2c4c6d607b72ffe6669009a44d2065a64df2fae83711b82` — full detail in `phase11/phase11_result.json`

## Phase 12 — Silicon — MIMXRT1060-EVK, RAM only (KAT, S3, S4, S5)

Result: ❌ FAIL

| Case | Check | Result |
|---|---|---|
| P12.1 | kat_bit_identical (rc=0): 7 PASS, 0 FAIL; 6 evidence files re-hashed | ✅ PASS |
| P12.2 | kat_bit_identical · PASS paquete silicio/kat coincide con su lista | ✅ PASS |
| P12.3 | kat_bit_identical · PASS candidate10 (sello 16) intacto | ✅ PASS |
| P12.4 | kat_bit_identical · PASS Mac = nube (digest sellado) | ✅ PASS |
| P12.5 | kat_bit_identical · PASS firmware compilado | ✅ PASS |
| P12.6 | kat_bit_identical · PASS ELF solo RAM: 136660 bytes cargables, tabla de vectores en OCRAM2 (probe-rs arranca desde RAM; la flash no se toca) | ✅ PASS |
| P12.7 | kat_bit_identical · PASS placa = Mac = nube: el kernel de produccion da los MISMOS bytes en el Cortex-M7 | ✅ PASS |
| P12.8 | kat_bit_identical · SILICIO KAT: PASS | ✅ PASS |
| P12.9 | s3_s4_s5 (rc=1): 15 PASS, 3 FAIL; 32 evidence files re-hashed | ❌ FAIL |
| P12.10 | s3_s4_s5 · PASS silicio/s345 coincide con su lista | ✅ PASS |
| P12.11 | s3_s4_s5 · PASS silicio/kat coincide con su lista | ✅ PASS |
| P12.12 | s3_s4_s5 · PASS candidate10 coincide con su lista | ✅ PASS |
| P12.13 | s3_s4_s5 · PASS replay_g_v2 coincide con su lista | ✅ PASS |
| P12.14 | s3_s4_s5 · PASS lean_g coincide con su lista | ✅ PASS |
| P12.15 | s3_s4_s5 · PASS trazas selladas de referencia: replay_g_v2_20261117T185851Z (SHA256SUMS integro) | ✅ PASS |
| P12.16 | s3_s4_s5 · PASS S4 en el simulador SNVS (A 18, B 5, corte, D 5) | ✅ PASS |
| P12.17 | s3_s4_s5 · PASS Mac (port sin editar, candidate10) = prefijo EXACTO de las trazas selladas (candidate8): 144145 bytes, 300 mundos | ✅ PASS |
| P12.18 | s3_s4_s5 · PASS S3 frecuencia del nucleo medida contra el RTC de 32768 Hz: 395991849 / 395991798 / 395991864 Hz (coinciden a 0,1 %) | ✅ PASS |
| P12.19 | s3_s4_s5 · PASS S3 ciclos por operacion: 6 medidas x (sin cache, con cache) | ✅ PASS |
| P12.20 | s3_s4_s5 · PASS S4-A en la placa: 18/18 (testigo perdido niega genesis y apertura; ceremonia; linaje sobre el contador; restaurar/clonar/split-brain negados). MC=11 | ✅ PASS |
| P12.21 | s3_s4_s5 · PASS S4-B: el contador sobrevivio al reset (11), almacen borrado/fabricado negado, ceremonia negada, contador sin moverse | ✅ PASS |
| P12.22 | s3_s4_s5 · PASS S5 trazas de la placa: sha256 en la placa = extraido = Mac = prefijo sellado (d5293e6b491ae7c55da9ec22b6271ba9e86abf05ed0995f82fa7b66512c3d552) | ✅ PASS |
| P12.23 | s3_s4_s5 · PASS S5 el reproductor DEMOSTRADO (applyG_sound) acepta las trazas de la placa: REPLAY G: PASS (toda transicion del Rust fue un Step del modelo G demostrado) | ✅ PASS |
| P12.24 | s3_s4_s5 · PASS control: la traza de la placa manipulada (contador +7) es RECHAZADA | ✅ PASS |
| P12.25 | s3_s4_s5 · FAIL fase lee: la placa no termino (ver placa_lee.txt) | ❌ FAIL |
| P12.26 | s3_s4_s5 · FAIL el SNVS no volvio al estado inicial | ❌ FAIL |
| P12.27 | s3_s4_s5 · SILICIO S3+S4+S5: FAIL | ❌ FAIL |

Phase seal: `73b5357cb071d60634375b5e34f486093f40574bb251929366fa73ca7b2d77cb` — full detail in `phase12/phase12_result.json`

## Scope (what this run does NOT claim)

- The composition 'every model-G guard is proved on the translated code ⇒ the code refines G' is ARGUED, not a single mechanized theorem; ReplayG (phase 7) is trace inclusion over the executed traces.
- Hardware (phase 12): the production kernel runs from RAM on the MIMXRT1060-EVK (nothing written to flash or fuses). Its freshness witness is the SNVS-LP monotonic counter: rollback-proof across resets, but LOST on power loss because the EVK has no battery on VDD_SNVS_IN; the kernel then refuses to open or start (fail-closed, proved in round 9), and only an operator ceremony starts a NEW lineage. Durability across power loss needs a battery-backed or external witness.
- The SNVS witness implementation (Rust glue reading the registers) is not translated to Lean: its contract is tested on a register simulator with 10 planted mutants and on the board; the kernel side is proved.
- Mutants outside model G's scope (M04, M08, M12, M13) are covered by the cohort campaign (phase 10), not by ReplayG.
- Amendment in force: E004 (ReplayG exporter: an injected anchor is emitted only when its signature is verifiably invalid).
