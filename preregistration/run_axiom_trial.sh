#!/usr/bin/env bash
# CNS AXIOM V3.4 — TRIAL (13 phases, 0-12; phase 12 = silicon on the MIMXRT1060-EVK, RAM only). Every phase re-executes its instrument or re-hashes its evidence IN THIS RUN.
# Writes trial/runs/AXIOM_TRIAL_<UTC>/ with phaseN/ results, AXIOM_REPORT.md/.txt, summary.json and the phase Merkle root.
# Official pair: first an OFFLINE run (network disconnected for the whole run), then an ONLINE run that re-checks against
# Bitcoin, pairs with the offline run (same sealed source) and stamps the trial manifest (which carries the offline manifest).
# Prerequisites: all seals closed in Bitcoin, campaign 0003 already run, the board connected by USB (phase 12 asks TWICE
# to unplug it for 10 s; the prompts appear in this terminal).
# Usage: bash /Volumes/CNS_SYSTEMS/AXIOM/axiom_v3_4/trial_v3/run_axiom_trial.sh offline|online
set -u
H="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; A="${AXIOM_ROOT:-$(cd "$H/.." && pwd)}"; T="${CNS_TOOLS:-$HOME/CNS_TOOLS}"
MODE="${1:-}"; case "$MODE" in offline|online) ;; *) echo "usage: bash run_axiom_trial.sh offline|online"; exit 1;; esac
GOV="$A/00_GOVERNANCE"; RID="AXIOM_TRIAL_$(date -u +%Y%m%dT%H%M%SZ)"; RD="$H/runs/$RID"; mkdir -p "$RD"
export PATH="$HOME/.elan/bin:$PATH" PYTHONDONTWRITEBYTECODE=1
[ "$MODE" = offline ] && export CARGO_NET_OFFLINE=true   # offline: cargo must never try the network
LIB=(python3 -I "$H/trial_lib.py")
out(){ echo "$*" | tee -a "$RD/trial_stdout.txt"; }
SHA(){ if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$@"; else sha256sum "$@"; fi; }
OTS=""; for c in "$HOME/.ots-venv/bin/ots" "$HOME/ots-env/bin/ots" "$(command -v ots 2>/dev/null)"; do [ -n "$c" ] && [ -x "$c" ] && { OTS="$c"; break; }; done
# run an instrument with a hard time limit (whole process group is killed on timeout)
corre(){ local secs="$1" log="$2"; shift 2
  perl -e '$t=shift; $p=fork; if(!$p){setpgrp(0,0); exec @ARGV} $SIG{ALRM}=sub{kill "KILL", -$p; exit 142}; alarm $t; waitpid($p,0); exit($?>>8)' "$secs" "$@" >"$log" 2>&1; }
inst(){ local ph="$1" name="$2" label="$3" secs="$4"; shift 4; local d="$RD/phase$ph" log="$RD/phase$ph/$label.log"; mkdir -p "$d"
  out "   - $label ..."; corre "$secs" "$log" "$@"; local rc=$?
  "${LIB[@]}" instrument "$ph" "$name" "$d" "$label" "$log" "$rc" | tee -a "$RD/trial_stdout.txt"; }
# interactive instrument (the board runner asks the operator to unplug the board): output goes to the log AND to this
# terminal, input comes from this terminal; same foreground process group (no setpgrp), so prompts and `read` work.
inst_tty(){ local ph="$1" name="$2" label="$3" script="$4"; local d="$RD/phase$ph" log="$RD/phase$ph/$label.log"; mkdir -p "$d"
  out "   - $label ..."; bash -o pipefail -c 'bash "$1" 2>&1 | { if (: > /dev/tty) 2>/dev/null; then tee /dev/tty; else cat; fi; }' _ "$script" > "$log" 2>&1; local rc=$?
  "${LIB[@]}" instrument "$ph" "$name" "$d" "$label" "$log" "$rc" | tee -a "$RD/trial_stdout.txt"; }
fase(){ out ""; out "== PHASE $1 — $2"; }

out "CNS AXIOM V3.4 — TRIAL — $RID — $(echo "$MODE" | tr a-z A-Z)"; out "root: $A"; out "utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
( cd "$H" && SHA -c EXPECTED_SHA256.txt ) >"$RD/trial_integrity.txt" 2>&1 && out "trial runner equals its sealed list" || { out "ABORT: the trial runner changed (trial/EXPECTED_SHA256.txt)"; exit 1; }

fase 0 "Network & Toolchain Status"; mkdir -p "$RD/phase0"; "${LIB[@]}" p0 "$RD/phase0" "$MODE" "$H/runs" "$A" | tee -a "$RD/trial_stdout.txt"
fase 1 "Sealed Source & Evidence Integrity"; mkdir -p "$RD/phase1"; "${LIB[@]}" p1 "$A" "$RD/phase1" | tee -a "$RD/trial_stdout.txt"

fase 2 "Production Kernel: candidate10 Build, Equivalence & Translation"
inst 2 c10 candidate10_pipeline 7200 bash "$A/candidate10/run_c10.sh"
"${LIB[@]}" close 2 "Production Kernel" "$RD/phase2" | tee -a "$RD/trial_stdout.txt"

fase 3 "Model Proofs (F1, F2, F3, F3b, G)"
inst 3 models lean_f1 1800 bash "$A/lean_f1/run_lean_f1.sh"
inst 3 models lean_f2 1800 bash "$A/lean_f2/run_lean_f2.sh"
inst 3 models lean_f3 3600 bash "$A/lean_f3/run_f3.sh"
inst 3 models lean_f3b 3600 bash "$A/lean_f3b/run_f3b.sh"
inst 3 models lean_g 1800 bash "$A/lean_g/run_g.sh"
"${LIB[@]}" close 3 "Model Proofs" "$RD/phase3" | tee -a "$RD/trial_stdout.txt"

fase 4 "Formal Proofs on the Translated Production Code"; mkdir -p "$RD/phase4"
if "${LIB[@]}" p4pre "$A" "$T" "$RD/phase4" | tee -a "$RD/trial_stdout.txt"; [ "${PIPESTATUS[0]}" = 0 ]; then
  for n in 4 5 6 7 8 9; do inst 4 proofs "pruebas_r$n" 3600 bash "$T/pruebas_r$n/reproducir.sh"; done
else out "   proof packages differ from the sealed copies: phase 4 FAILS without running them"
  echo '{"instrument":"precheck","rc":1,"result":"FAIL","cases":[],"evidence":[],"log_sha256":""}' >> "$RD/phase4/phase4_instruments.jsonl"; fi
cat "$RD"/phase4/pruebas_r*.log > "$RD/phase4/all_proofs.log" 2>/dev/null
"${LIB[@]}" close 4 "Formal Proofs on Translated Code" "$RD/phase4" | tee -a "$RD/trial_stdout.txt"

fase 5 "Independent Verification (Python, own Ed25519)"
inst 5 verifier verifier_f3 3600 bash "$A/verifier_f3/run_verifier.sh"
"${LIB[@]}" close 5 "Independent Verification" "$RD/phase5" | tee -a "$RD/trial_stdout.txt"

fase 6 "Model-Code Bridge (model G guards)"; mkdir -p "$RD/phase6"
"${LIB[@]}" p6 "$T" "$RD/phase4/all_proofs.log" "$RD/phase6" | tee -a "$RD/trial_stdout.txt"

fase 7 "ReplayG — Code-to-Model Conformance"
inst 7 replayg replay_g_v2 7200 bash "$A/replay_g_v2/run_replay_g.sh"
"${LIB[@]}" close 7 "ReplayG" "$RD/phase7" | tee -a "$RD/trial_stdout.txt"

fase 8 "Determinism — Cross-Time Bit-Identical Replay"; mkdir -p "$RD/phase8"
p8(){ set -u; local W; W="$(mktemp -d)"; trap 'rm -rf "$W"' RETURN
  local SE; SE="$(grep -oE 'evidence/verifier_f3_[0-9TZ]+/traces.txt.gz' "$GOV/proofs/SEAL13_MANIFEST.txt" | head -1)"
  local want; want="$(grep "  $SE\$" "$GOV/proofs/SEAL13_MANIFEST.txt" | cut -c1-64)"
  [ -n "$SE" ] && [ "$(SHA "$A/$SE" | cut -c1-64)" = "$want" ] && echo "PASS sealed reference traces (seal 13) intact: $SE" || { echo "FAIL sealed reference traces missing/changed"; return 1; }
  cp -R "$A/verifier_f3/gen" "$W/gen"; sed "s#@KERNEL_PATH@#$A/candidate8/existence-kernel#" "$W/gen/Cargo.toml.in" > "$W/gen/Cargo.toml"
  ( cd "$W/gen" && CARGO_TARGET_DIR="$W/t" cargo build --offline --release ) >"$RD/phase8/build.txt" 2>&1 && echo "PASS sealed exporter rebuilt from source" || { echo "FAIL exporter build"; return 1; }
  env -u AXIOM_SEED "$W/t/release/axiom-cohorts" CONFORM --worlds 3000 --events 40 --out "$W/now.txt" | sed 's#-> .*#-> (this run)#'
  gzip -dc "$A/$SE" > "$W/then.txt"; local a b; a="$(SHA "$W/then.txt" | cut -c1-64)"; b="$(SHA "$W/now.txt" | cut -c1-64)"
  [ "$a" = "$b" ] && echo "PASS 3000 adversarial worlds regenerated now are BIT-IDENTICAL to the traces sealed in seal 13 (sha256 $a)" || { echo "FAIL traces differ: sealed=$a now=$b"; return 1; }
  ( cd "$RD/phase8" && SHA build.txt > SHA256SUMS ); echo "evidencia: $RD/phase8"; echo "DETERMINISM: PASS"; }
p8 > "$RD/phase8/determinism.log" 2>&1; rc=$?
"${LIB[@]}" instrument 8 determinism "$RD/phase8" determinism "$RD/phase8/determinism.log" "$rc" | tee -a "$RD/trial_stdout.txt"
"${LIB[@]}" close 8 "Determinism" "$RD/phase8" | tee -a "$RD/trial_stdout.txt"

fase 12 "Silicon — MIMXRT1060-EVK, RAM only (KAT, S3 timing, S4 hardware witness, S5 ReplayG from the board)"
out "   the board must be connected by USB; the S3-S5 instrument asks TWICE to unplug it for 10 s (follow the prompts)"
[ -e /dev/tty ] || out "   WARNING: no terminal: the board prompts cannot be answered"
inst_tty 12 silicon kat_bit_identical "$A/silicio/kat/run_kat_placa.sh"
inst_tty 12 silicon s3_s4_s5 "$A/silicio/s345/run_s345_placa.sh"
"${LIB[@]}" close 12 "Silicon" "$RD/phase12" | tee -a "$RD/trial_stdout.txt"

fase 9 "Red Team — Planted-Fault Matrix"; mkdir -p "$RD/phase9"
for ph in 3 4 5 7 12; do cp "$RD/phase$ph/phase${ph}_instruments.jsonl" "$RD/phase9/" 2>/dev/null; done
"${LIB[@]}" p9 "$RD/phase9" | tee -a "$RD/trial_stdout.txt"

fase 10 "Bitcoin-Seeded Adversarial Campaign 0003"; mkdir -p "$RD/phase10"
"${LIB[@]}" p10 "$A" "${OTS:-ots}" "$RD/phase10" "$MODE" | tee -a "$RD/trial_stdout.txt"

fase 11 "Seal Chain & Non-Regression (Bitcoin)"; mkdir -p "$RD/phase11"
"${LIB[@]}" p11 "$A" "$GOV" "$RD/phase11" "$MODE" | tee -a "$RD/trial_stdout.txt"

out ""; out "== REPORT"
"${LIB[@]}" report "$RD" "$A" "$MODE" | tee -a "$RD/trial_stdout.txt"; rc=${PIPESTATUS[0]}
if [ "$MODE" = online ]; then python3 -I -c "import json,sys;p=json.load(open(sys.argv[1])).get('pair_offline_run') or {};print(p.get('run','NONE'));print(p.get('trial_manifest_sha256',''))" "$RD/phase0/phase0_result.json" > "$RD/PAIR.txt"; fi
out "run: $RD"
# the manifest is written LAST: nothing inside the run directory changes after it (stamp messages go to SEAL_LOG.txt, outside the manifest)
( cd "$RD" && find . -type f ! -name TRIAL_MANIFEST.txt ! -name SEAL_LOG.txt ! -name '*.ots' | sort | while IFS= read -r f; do SHA "$f"; done > TRIAL_MANIFEST.txt )
sl(){ echo "$*" | tee -a "$RD/SEAL_LOG.txt"; }
sl "trial manifest: $(SHA "$RD/TRIAL_MANIFEST.txt" | cut -c1-64)"
if [ "$MODE" = offline ]; then sl "OFFLINE run: no stamp here; the ONLINE run of the pair carries this manifest and stamps it"
elif [ $rc = 0 ] && [ -n "$OTS" ]; then "$OTS" stamp "$RD/TRIAL_MANIFEST.txt" >/dev/null 2>&1 && sl "TRIAL_MANIFEST.txt stamped with OpenTimestamps (Bitcoin attestation pending; close with close_all_seals.sh)" || sl "WARNING: could not stamp the trial manifest"; fi
exit $rc
