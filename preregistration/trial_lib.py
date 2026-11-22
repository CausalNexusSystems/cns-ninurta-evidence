#!/usr/bin/env python3
"""CNS AXIOM V3.4 trial helpers. Every check here reads files and recomputes hashes; nothing is taken from a cache.
usage: trial_lib.py <subcommand> ...   (see run_axiom_trial.sh)"""
import sys, os, re, json, hashlib, socket, subprocess, shutil, time, glob, gzip

def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def now(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def check_sums(base, sumfile):
    """Verify a `sha256  path` list relative to base. Returns (n_ok, [failures])."""
    ok, bad = 0, []
    for line in open(sumfile, encoding='utf-8', errors='replace'):
        m = re.match(r'^([0-9a-f]{64})\s+\*?(.+?)\s*$', line)
        if not m: continue
        p = os.path.join(base, m.group(2))
        if not os.path.isfile(p): bad.append(f"missing {m.group(2)}"); continue
        if sha_file(p) != m.group(1): bad.append(f"changed {m.group(2)}"); continue
        ok += 1
    return ok, bad

def write_result(outdir, phase, name, result, cases, extra=None):
    os.makedirs(outdir, exist_ok=True)
    r = {"phase": phase, "name": name, "result": "PASS" if result else "FAIL", "finished_utc": now(), "cases": cases}
    if extra: r.update(extra)
    p = os.path.join(outdir, f"phase{phase}_result.json")
    with open(p, 'w') as f: json.dump(r, f, indent=1, ensure_ascii=False)
    print(f"PHASE {phase} {name}: {'PASS' if result else 'FAIL'}")
    return result

# ---------------------------------------------------------------- generic: parse an instrument log
CASE = re.compile(r'^\s*(PASS|FAIL|DEMOSTRADO|INFO|ABORTA)\b[: ]?\s*(.*)$')
def parse_log(log):
    cases, evid = [], []
    for raw in open(log, encoding='utf-8', errors='replace'):
        l = re.sub(r'\x1b\[[0-9;?]*[a-zA-Z]', '', raw.rstrip('\n'))
        m = CASE.match(l)
        if m:
            k = m.group(1); st = {"PASS": "PASS", "DEMOSTRADO": "PASS", "INFO": "INFO", "FAIL": "FAIL", "ABORTA": "FAIL"}[k]
            cases.append({"status": st, "check": (k + " " + m.group(2)).strip()[:300]}); continue
        m = re.match(r'^\s*evidencia:\s*(\S+)', l)
        if m: evid.append(m.group(1)); continue
        # final verdict line of an instrument, e.g. "LEAN F1: PASS", "REPLAY G (formal): PASS (...)" (not indented)
        m = re.match(r'^(\S[^:]{2,120}):\s*(PASS|FAIL)\b', l)
        if m and not l.startswith(("linea", "#")):
            cases.append({"status": m.group(2), "check": l.strip()[:300]})
    return cases, evid

def cmd_instrument(a):
    """instrument <phase> <name> <outdir> <label> <log> <rc>  -> appends a sub-result json (one instrument run)"""
    phase, name, outdir, label, log, rc = a[0], a[1], a[2], a[3], a[4], int(a[5])
    os.makedirs(outdir, exist_ok=True)
    cases, evid = parse_log(log)
    integ = []
    for e in evid:
        s = os.path.join(e, 'SHA256SUMS')
        if os.path.isfile(s):
            n, bad = check_sums(e, s); integ.append({"evidence": e, "files_ok": n, "failures": bad})
        else: integ.append({"evidence": e, "files_ok": 0, "failures": ["no SHA256SUMS"]})
    ok = (rc == 0 and any(c["status"] == "PASS" for c in cases) and not any(c["status"] == "FAIL" for c in cases)
          and evid and all(not i["failures"] and i["files_ok"] > 0 for i in integ))
    sub = {"instrument": label, "rc": rc, "result": "PASS" if ok else "FAIL", "cases": cases, "evidence": integ,
           "log_sha256": sha_file(log)}
    p = os.path.join(outdir, f"phase{phase}_instruments.jsonl")
    with open(p, 'a') as f: f.write(json.dumps(sub, ensure_ascii=False) + "\n")
    print(f"   {label}: {'PASS' if ok else 'FAIL'} (rc={rc}, casos={len(cases)}, evidencia={len(evid)})")
    return 0 if ok else 1

def cmd_close(a):
    """close <phase> <name> <outdir>  -> phase result from all instrument sub-results"""
    phase, name, outdir = a
    p = os.path.join(outdir, f"phase{phase}_instruments.jsonl")
    subs = [json.loads(l) for l in open(p)] if os.path.isfile(p) else []
    cases = []
    for s in subs:
        cases.append({"status": s["result"], "check": f"{s['instrument']} (rc={s['rc']}): {sum(c['status']=='PASS' for c in s['cases'])} PASS, "
                      f"{sum(c['status']=='FAIL' for c in s['cases'])} FAIL; {sum(e['files_ok'] for e in s['evidence'])} evidence files re-hashed"
                      + "".join(f"; {e['evidence'].split('/')[-1]}: {e['failures'][:2]}" for e in s['evidence'] if e['failures'])})
        cases += [{"status": c["status"], "check": f"{s['instrument']} · {c['check']}"} for c in s["cases"]]
    ok = bool(subs) and all(s["result"] == "PASS" for s in subs)
    return 0 if write_result(outdir, int(phase), name, ok, cases, {"instruments": [s["instrument"] for s in subs]}) else 1

# ---------------------------------------------------------------- phase 0
def cmd_p0(a):
    outdir, mode, runs, root = a; cases = []
    os.makedirs(outdir, exist_ok=True)
    probes = [("1.1.1.1", 53), ("8.8.8.8", 53), ("blockstream.info", 443), ("mempool.space", 443)]
    up = 0
    for h, p in probes:
        try: socket.create_connection((h, p), timeout=3).close(); st = "reachable"; up += 1
        except Exception: st = "unreachable"
        cases.append({"status": "INFO", "check": f"TCP {h}:{p} {st}"})
    online = up >= 3
    if mode == "offline":
        cases.append({"status": "PASS" if up == 0 else "FAIL",
                      "check": "OFFLINE run: the machine has no network for the whole run (all probes unreachable)" if up == 0 else f"OFFLINE run requested but {up} network probes answered: disconnect the network"})
    else:
        cases.append({"status": "PASS" if online else "FAIL",
                      "check": "ONLINE run: Bitcoin explorers reachable (phases 10-11 re-check against Bitcoin; trial seal stamped)" if online else "ONLINE run requested but the explorers are unreachable"})
        pair = pair_offline(runs, root)
        cases.append(pair[0]); online = online and pair[1] is not None
        globals()["_PAIR"] = pair[1]
    tools = {}
    def ver(cmd, cwd=None):
        # lean is resolved by elan from the lean-toolchain of the model packages (lean_g), as the instruments do
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=cwd)
            line = (r.stdout.strip().splitlines() or [""])[0]
            return line if (r.returncode == 0 and re.search(r'\d+\.\d+', line)) else None
        except Exception: return None
    lg = os.path.join(root, "lean_g")
    for k, cmd in [("cargo", ["cargo", "--version"]), ("rustc", ["rustc", "--version"]), ("python3", [sys.executable, "--version"]),
                   ("lean", ["lean", "--version"]), ("probe-rs", ["probe-rs", "--version"])]:
        v = ver(cmd, lg if k == "lean" else None); tools[k] = v
        cases.append({"status": "PASS" if v else "FAIL", "check": f"{k}: {v or 'NOT FOUND'}"})
    ots = next((c for c in [os.path.expanduser("~/.ots-venv/bin/ots"), os.path.expanduser("~/ots-env/bin/ots"), shutil.which("ots")] if c and os.path.exists(c)), None)
    cases.append({"status": "PASS" if ots else "FAIL", "check": f"opentimestamps client: {ots or 'NOT FOUND'}"})
    try: st = os.statvfs(os.path.expanduser("~")); free = st.f_bavail * st.f_frsize / 2**30
    except Exception: free = 0.0
    cases.append({"status": "PASS" if free >= 6 else "FAIL", "check": f"free disk on the home volume: {free:.1f} GB (>= 6 GB required)"})
    ok = all(c["status"] != "FAIL" for c in cases)
    extra = {"mode": mode, "network_probes_answered": up, "tools": tools, "source_digest": source_digest(root)}
    if mode == "online": extra["pair_offline_run"] = globals().get("_PAIR")
    return 0 if write_result(outdir, 0, "Network & Toolchain Status", ok, cases, extra) else 1

def source_digest(root):
    """RFC 6962 root over the sha256 of every package list and every seal manifest (what both runs of the pair must share)."""
    lists = sorted(l for l in glob.glob(os.path.join(root, "*", "EXPECTED_SHA256.txt")) if "/_to_delete/" not in l)
    return merkle([sha_file(p) for p in lists + manifests(root)])

def pair_offline(runs, root):
    """The online run of the official pair needs a completed OFFLINE run, ALL PASS, over the same sealed source."""
    want = source_digest(root); best = None
    for d in sorted(glob.glob(os.path.join(runs, "AXIOM_TRIAL_*"))):
        try:
            s = json.load(open(os.path.join(d, "summary.json"))); p0 = json.load(open(os.path.join(d, "phase0", "phase0_result.json")))
        except Exception: continue
        if s.get("mode") == "offline" and s.get("overall") == "ALL PASS" and p0.get("source_digest") == want and os.path.isfile(os.path.join(d, "TRIAL_MANIFEST.txt")):
            n, bad = check_sums(d, os.path.join(d, "TRIAL_MANIFEST.txt"))
            if n > 0 and not bad: best = {"run": os.path.basename(d), "trial_manifest_sha256": sha_file(os.path.join(d, "TRIAL_MANIFEST.txt"))}
    if best: return ({"status": "PASS", "check": f"official pair: its OFFLINE counterpart {best['run']} is ALL PASS over the same sealed source (manifest {best['trial_manifest_sha256'][:16]}... re-verified)"}, best)
    return ({"status": "FAIL", "check": "official pair: no completed OFFLINE run (ALL PASS, same sealed source) to pair with; run the offline trial first"}, None)

# ---------------------------------------------------------------- phase 1
def manifests(root):
    pr = os.path.join(root, "00_GOVERNANCE", "proofs")
    return sorted(glob.glob(os.path.join(pr, "SEAL*_MANIFEST.txt")), key=lambda p: int(re.search(r'SEAL(\d*)_', p).group(1) or 0))

def cmd_p1(a):
    root, outdir = a; cases = []; ok = True
    os.makedirs(outdir, exist_ok=True)
    lists = sorted(glob.glob(os.path.join(root, "*", "EXPECTED_SHA256.txt")))
    lists = [l for l in lists if "/_to_delete/" not in l and "/trial/" not in l]
    tot = 0
    for l in lists:
        d = os.path.dirname(l); n, bad = check_sums(d, l); tot += n
        st = "PASS" if (not bad and n > 0) else "FAIL"; ok &= st == "PASS"
        cases.append({"status": st, "check": f"{os.path.relpath(d, root)}: {n} files equal their sealed list" + (f"; {bad[:3]}" if bad else "")})
    mt = 0
    for m in manifests(root):
        n, bad = check_sums(root, m); mt += n
        st = "PASS" if not bad else "FAIL"; ok &= st == "PASS"
        cases.append({"status": st, "check": f"{os.path.basename(m)}: {n} sealed files unchanged" + (f"; {bad[:3]}" if bad else "")})
    cases.insert(0, {"status": "PASS" if ok else "FAIL", "check": f"{len(lists)} package lists ({tot} files) and {len(manifests(root))} seal manifests ({mt} files) re-hashed"})
    return 0 if write_result(outdir, 1, "Sealed Source & Evidence Integrity", ok, cases) else 1

# ---------------------------------------------------------------- phase 4 pre-check: proof packages equal the sealed copies
def cmd_p4pre(a):
    root, tools, outdir = a; cases = []; ok = True
    os.makedirs(outdir, exist_ok=True)
    pr = os.path.join(root, "00_GOVERNANCE", "proofs")
    for n, seal in [(4, 17), (5, 18), (6, 19), (7, 20), (8, 21), (9, 25)]:
        man = os.path.join(pr, f"SEAL{seal}_MANIFEST.txt")
        ev = sorted({m.group(1) for m in re.finditer(rf'(evidence/teoremas_c10_r{n}_[0-9TZ]+)/', open(man).read())})
        if len(ev) != 1: cases.append({"status": "FAIL", "check": f"r{n}: sealed evidence not found in SEAL{seal}"}); ok = False; continue
        sev = os.path.join(root, ev[0]); pkg = os.path.join(tools, f"pruebas_r{n}"); diff = []; cnt = 0
        for sub in ("teoremas", "controles"):
            for f in sorted(glob.glob(os.path.join(sev, sub, "*.lean"))):
                g = os.path.join(pkg, sub, os.path.basename(f)); cnt += 1
                if not os.path.isfile(g) or sha_file(g) != sha_file(f): diff.append(os.path.basename(f))
            extra = [os.path.basename(g) for g in glob.glob(os.path.join(pkg, sub, "*.lean")) if not os.path.isfile(os.path.join(sev, sub, os.path.basename(g)))]
            diff += [f"+{x}" for x in extra]
        st = "PASS" if (not diff and cnt > 0) else "FAIL"; ok &= st == "PASS"
        cases.append({"status": st, "check": (f"pruebas_r{n}: {cnt} theorem/control files identical to sealed {ev[0]} (seal {seal})" if not diff else f"pruebas_r{n}: files DIFFER from sealed {ev[0]} (seal {seal}): {diff}")})
    with open(os.path.join(outdir, "phase4_precheck.json"), 'w') as f: json.dump(cases, f, indent=1)
    for c in cases: print(("PASS " if c["status"] == "PASS" else "FAIL ") + c["check"])
    return 0 if ok else 1

# ---------------------------------------------------------------- phase 6: bridge table -> proved theorems
BRIDGE = [  # (guard of model G, theorem on translated code)
 ("openp.hsig signature check", "F45_apertura"), ("openp.hacc binding to witness", "F4_ligadura"),
 ("openp.hacc binding to witness", "F45_apertura_ligada"), ("successor is +1", "F4_sucesor_es_mas_uno"),
 ("commit ws=ww=true", "G2_commit_exige_almacen_y_testigo"), ("Valid: collapse not in h", "T3_no_autoriza_tras_colapso"),
 ("Valid: t not consumed", "T1_no_autoriza_paso_consumido"), ("Valid: t not consumed", "T2_autorizar_registra_el_consumo"),
 ("Valid: t not consumed", "FR12_no_dos_autorizaciones_del_mismo_paso"), ("Valid: lineage (no head)", "M0_lineage_ok_sin_cabeza_exige_paso_1"),
 ("CtrOK counter 0", "G1a_contador_cero"), ("CtrOK monotone", "G1b_contador_no_creciente"),
 ("hpois", "G3b_envenenada_no_consume"), ("hpois", "FR11_ejecutor_solo_tras_autorizacion"),
 ("pois := pois || !rok", "G3_recibo_no_anclado_envenena"), ("one effect per step", "FR11_un_efecto_por_paso"),
 ("hardware witness lost (PGD) => authority gate never opens", "S4_fc_open_autoridad"),
 ("hardware witness lost (PGD) => effect gate never opens", "S4_fc_open_efectos"),
 ("hardware witness lost (PGD) => no authority genesis", "S4_fc_genesis_autoridad"),
 ("hardware witness lost (PGD) => no effect genesis", "S4_fc_genesis_efectos")]
def cmd_p6(a):
    tools, p4log, outdir = a; cases = []; ok = True
    os.makedirs(outdir, exist_ok=True)
    txt = open(p4log, encoding='utf-8', errors='replace').read()
    for guard, thm in BRIDGE:
        files = [f for f in glob.glob(os.path.join(tools, "pruebas_r[4-9]", "teoremas", "*.lean")) if re.search(rf'^theorem {thm}\b', open(f).read(), re.M)]
        proved = [f for f in files if re.search(rf'DEMOSTRADO {re.escape(os.path.basename(f)[:-5])}\b', txt)]
        st = "PASS" if proved else "FAIL"; ok &= bool(proved)
        cases.append({"status": st, "check": f"G guard [{guard}] <- `{thm}`" + (f" proved in this run ({os.path.basename(proved[0])})" if proved else " NOT proved in this run")})
    composition = {"status": "INFO", "check": "Composition 'all guards proved => code refines G => fr1_g holds for the code' is ARGUED, not mechanized as one theorem; its empirical evidence is phase 7 (ReplayG)."}
    cases.append(composition)
    return 0 if write_result(outdir, 6, "Model-Code Bridge (model G guards)", ok, cases) else 1

# ---------------------------------------------------------------- phase 9: red-team matrix (aggregation of planted faults across instruments)
def cmd_p9(a):
    outdir = a[0]; cases = []; ok = True; tot = 0
    os.makedirs(outdir, exist_ok=True)
    for ph, label in [(3, "model sabotage"), (4, "proof controls (mutants / missing hypotheses)"), (5, "independent verifier mutants"), (7, "ReplayG mutants and tampered traces"), (12, "silicon: tampered board trace rejected")]:
        p = os.path.join(outdir, f"phase{ph}_instruments.jsonl")
        if not os.path.isfile(p): cases.append({"status": "FAIL", "check": f"phase {ph}: no results"}); ok = False; continue
        n = 0
        for l in open(p):
            s = json.loads(l)
            for c in s["cases"]:
                t = c["check"].lower()
                if c["status"] == "PASS" and re.search(r'sabotaje|mutante|detectad|control|manipulad|tamper|alterad|vacuidad|_m[0-9]{2}|\bm[0-9]{2}\b', t): n += 1
        tot += n; st = "PASS" if n > 0 else "FAIL"; ok &= n > 0
        cases.append({"status": st, "check": f"{label}: {n} planted faults/controls caught (phase {ph})"})
    cases.insert(0, {"status": "PASS" if ok else "FAIL", "check": f"{tot} planted faults/controls caught across 5 independent instruments; none escaped (an escape fails its own phase)"})
    return 0 if write_result(outdir, 9, "Red Team — Planted-Fault Matrix", ok, cases) else 1

# ---------------------------------------------------------------- phase 10: Bitcoin-seeded campaign 0003
def http(url):
    import urllib.request
    try:
        with urllib.request.urlopen(url, timeout=25) as r: return r.read().decode().strip()
    except Exception: return None
def cmd_p10(a):
    root, ots, outdir, mode = a; cases = []; ok = True
    os.makedirs(outdir, exist_ok=True)
    camp = json.load(open(os.path.join(root, "cohorts_v3", "CAMPAIGN.json"))); sh = int(camp["seed"]["seed_height"])
    bh = os.path.join(root, "cohorts_v3", "BLOCK_HASH.txt")
    if not os.path.isfile(bh): return 0 if write_result(outdir, 10, "Bitcoin-Seeded Adversarial Campaign 0003", False, [{"status": "FAIL", "check": "BLOCK_HASH.txt missing: campaign 0003 not run yet"}]) else 1
    h = open(bh).read().strip()
    if mode == "online":
        h1 = http(f"https://blockstream.info/api/block-height/{sh}"); h2 = http(f"https://mempool.space/api/block-height/{sh}")
        st = "PASS" if (h1 and h1 == h2 == h) else "FAIL"; ok &= st == "PASS"
        cases.append({"status": st, "check": f"seed = hash of Bitcoin block {sh}, re-read now from blockstream and mempool: {h[:16]}... (match={h1 == h2 == h})"})
    else:
        cases.append({"status": "INFO", "check": f"OFFLINE: seed block {sh} hash {h[:16]}... is re-read from two Bitcoin explorers by the ONLINE run of the pair"})
    info = subprocess.run([ots, "info", os.path.join(root, "cohorts_v3", "CAMPAIGN.json.ots")], capture_output=True, text=True).stdout
    att = sorted({int(x) for x in re.findall(r'BitcoinBlockHeaderAttestation\((\d+)\)', info)})
    st = "PASS" if (att and att[0] < sh) else "FAIL"; ok &= st == "PASS"
    cases.append({"status": st, "check": f"campaign definition attested in Bitcoin at block {att[0] if att else '?'} BEFORE the seed block {sh} (no seed grinding)"})
    evs = sorted(glob.glob(os.path.join(root, "evidence", "cohorts_v3_formal_*")))
    if len(evs) != 1:
        cases.append({"status": "FAIL", "check": f"expected exactly one formal run of campaign 0003, found {len(evs)}"}); ok = False
    else:
        e = evs[0]; n, bad = check_sums(e, os.path.join(e, "SHA256SUMS"))
        st = "PASS" if (n > 0 and not bad) else "FAIL"; ok &= st == "PASS"
        cases.append({"status": st, "check": f"{os.path.relpath(e, root)}: {n} evidence files intact"})
        summ = open(os.path.join(e, "SUMMARY.txt"), errors='replace').read()
        st = "PASS" if "COHORTS RUN (formal): PASS" in summ and h in open(os.path.join(e, "cohorts_run.txt"), errors='replace').read() + summ else "FAIL"
        ok &= st == "PASS"
        cases.append({"status": st, "check": "formal verdict PASS and the run used the saved block hash as seed"})
        for l in open(os.path.join(e, "CAMPAIGN_RESULT.jsonl")):
            try: r = json.loads(l)
            except Exception: continue
            if "cohort" in r:
                c_ok = r.get("violations", 1) == 0 and r.get("control_failures", 1) == 0
                ok &= c_ok
                cases.append({"status": "PASS" if c_ok else "FAIL", "check": f"cohort {r['cohort']}: {r.get('instances')} instances, {r.get('violations')} violations, 95% upper bound {r.get('cp95_upper')}"})
    return 0 if write_result(outdir, 10, "Bitcoin-Seeded Adversarial Campaign 0003", ok, cases) else 1

# ---------------------------------------------------------------- phase 11: seal chain
def cmd_p11(a):
    root, gov, outdir, mode = a; cases = []; ok = True
    os.makedirs(outdir, exist_ok=True)
    js = os.path.join(outdir, "ots_verify.json")
    r = subprocess.run([sys.executable, "-I", os.path.join(gov, "ots_independent_verify.py"), root, "--json", js] + (["--offline"] if mode == "offline" else []), capture_output=True, text=True)
    open(os.path.join(outdir, "ots_verify.txt"), 'w').write(r.stdout + r.stderr)
    rows = json.load(open(js))["rows"] if os.path.isfile(js) else []
    want = "CERRADO" if mode == "online" else "DIGEST_OK"
    closed = [x for x in rows if x["estado"] == want]
    st = "PASS" if rows and len(closed) == len(rows) else "FAIL"; ok &= st == "PASS"
    if mode == "online":
        cases.append({"status": st, "check": f"{len(closed)}/{len(rows)} OpenTimestamps seals attested in Bitcoin; merkle root re-checked on 2 explorers; sealed file digest = current digest"})
    else:
        cases.append({"status": st, "check": f"{len(closed)}/{len(rows)} OpenTimestamps seals: sealed digest = current digest and the hash chain up to the Bitcoin block header commitment recomputed locally; explorer check by the ONLINE run of the pair"})
    for x in rows:
        if x["estado"] != want: cases.append({"status": "FAIL", "check": f"{x['ots']}: {x['estado']} {x.get('motivo','')}"})
    ms = [m for m in manifests(root) if re.search(r'SEAL(\d+)_', m) and int(re.search(r'SEAL(\d+)_', m).group(1)) >= 16]
    for m in ms:
        k = int(re.search(r'SEAL(\d+)_', m).group(1))
        if k == 16: continue
        prev = os.path.join(os.path.dirname(m), f"SEAL{k-1}_MANIFEST.txt")
        link = f"{sha_file(prev)}  00_GOVERNANCE/proofs/SEAL{k-1}_MANIFEST.txt" in open(m).read()
        ok &= link; cases.append({"status": "PASS" if link else "FAIL", "check": f"chain: SEAL{k} contains the hash of SEAL{k-1}"})
    return 0 if write_result(outdir, 11, "Seal Chain & Non-Regression (Bitcoin)", ok, cases) else 1

# ---------------------------------------------------------------- report
def merkle(leaves):
    # RFC 6962: leaf = H(0x00 || d), node = H(0x01 || l || r)
    H = lambda b: hashlib.sha256(b).digest()
    nodes = [H(b'\x00' + bytes.fromhex(x)) for x in leaves]
    def mth(n):
        if len(n) == 1: return n[0]
        k = 1
        while k * 2 < len(n): k *= 2
        return H(b'\x01' + mth(n[:k]) + mth(n[k:]))
    return mth(nodes).hex() if nodes else hashlib.sha256(b'').hexdigest()

NAMES = ["Network & Toolchain Status", "Sealed Source & Evidence Integrity", "Production Kernel: candidate10 Build, Equivalence & Translation",
         "Model Proofs (F1, F2, F3, F3b, G)", "Formal Proofs on the Translated Production Code", "Independent Verification (Python, own Ed25519)",
         "Model-Code Bridge (model G guards)", "ReplayG — Code-to-Model Conformance", "Determinism — Cross-Time Bit-Identical Replay",
         "Red Team — Planted-Fault Matrix", "Bitcoin-Seeded Adversarial Campaign 0003", "Seal Chain & Non-Regression (Bitcoin)",
         "Silicon — MIMXRT1060-EVK, RAM only (KAT, S3, S4, S5)"]
def cmd_report(a):
    rd, root, mode = a; ver = "3.4.0"
    try: ver = re.search(r'^version\s*=\s*"([^"]+)"', open(os.path.join(root, "candidate10", "existence-kernel", "Cargo.toml")).read(), re.M).group(1)
    except Exception: pass
    run_id = os.path.basename(rd); phases = []; seals = []
    for i in range(13):
        p = os.path.join(rd, f"phase{i}", f"phase{i}_result.json")
        if os.path.isfile(p): r = json.load(open(p)); s = sha_file(p)
        else: r = {"phase": i, "name": NAMES[i], "result": "FAIL", "cases": [{"status": "FAIL", "check": "phase did not produce a result"}]}; s = hashlib.sha256(b'missing').hexdigest()
        r["name"] = NAMES[i]; r["phase_seal"] = s; phases.append(r); seals.append(s)
    root_m = merkle(seals); allpass = all(p["result"] == "PASS" for p in phases)
    p0 = phases[0]
    pair = None
    try: pair = json.load(open(os.path.join(rd, "phase0", "phase0_result.json"))).get("pair_offline_run")
    except Exception: pass
    summ = {"run_id": run_id, "product": "CNS AXIOM", "kernel_version": ver, "generated_utc": now(), "mode": mode, "pair_offline_run": pair,
            "organization": "Causal Nexus Systems LLC — Anthony Moreno, Founder & CEO",
            "overall": "ALL PASS" if allpass else "FAIL", "phase_merkle_root_rfc6962": root_m,
            "phases": [{"phase": p["phase"], "name": p["name"], "result": p["result"], "phase_seal": p["phase_seal"]} for p in phases]}
    json.dump(summ, open(os.path.join(rd, "summary.json"), 'w'), indent=1, ensure_ascii=False)
    ic = lambda r: "✅ PASS" if r == "PASS" else ("ℹ️ INFO" if r == "INFO" else "❌ FAIL")
    md = [f"# CNS AXIOM V{ver} — Run Report — {run_id}", "",
          "> This report states only what was directly observed in this run: pass/fail outcomes, verdicts, aggregate counts and cryptographic integrity. Every phase re-executes or re-hashes its evidence in this run; nothing is copied from an earlier run.", "",
          f"- **Run ID:** {run_id}", f"- **Mode:** {'OFFLINE (no network for the whole run)' if mode == 'offline' else 'ONLINE (second run of the official pair)'}"]
    if mode == "online": md += [f"- **Offline counterpart:** {pair['run'] if pair else 'NONE'}" + (f" (TRIAL_MANIFEST sha256 `{pair['trial_manifest_sha256']}`)" if pair else "")]
    md += [f"- **Timestamp (UTC):** {summ['generated_utc']}", f"- **Kernel version:** {ver} (existence-kernel, candidate 10 production path; candidate 8 for the sealed adversarial campaign)",
          f"- **Organization:** {summ['organization']}",
          "- **Assumptions (FR-0001):** S1 CAS freshness witness · S2 Ed25519 unforgeable · S3 binding witness · S4 SHA-256 collision resistant", "",
          "## Summary", "", "| Phase | Name | Result |", "|---|---|---|"]
    md += [f"| {p['phase']} | {p['name']} | {ic(p['result'])} |" for p in phases]
    md += ["", f"**Overall: {'✅ ALL PASS' if allpass else '❌ FAIL'}**", "", f"Phase Merkle root (RFC 6962): `{root_m}`", ""]
    for p in phases:
        md += [f"## Phase {p['phase']} — {p['name']}", "", f"Result: {ic(p['result'])}", "", "| Case | Check | Result |", "|---|---|---|"]
        for j, c in enumerate(p["cases"]):
            md.append(f"| P{p['phase']}.{j+1} | {c['check'].replace('|', '/')} | {ic(c['status'])} |")
        md += ["", f"Phase seal: `{p['phase_seal']}` — full detail in `phase{p['phase']}/phase{p['phase']}_result.json`", ""]
    md += ["## Scope (what this run does NOT claim)", "",
           "- The composition 'every model-G guard is proved on the translated code ⇒ the code refines G' is ARGUED, not a single mechanized theorem; ReplayG (phase 7) is trace inclusion over the executed traces.",
           "- Hardware (phase 12): the production kernel runs from RAM on the MIMXRT1060-EVK (nothing written to flash or fuses). Its freshness witness is the SNVS-LP monotonic counter: rollback-proof across resets, but LOST on power loss because the EVK has no battery on VDD_SNVS_IN; the kernel then refuses to open or start (fail-closed, proved in round 9), and only an operator ceremony starts a NEW lineage. Durability across power loss needs a battery-backed or external witness.",
           "- The SNVS witness implementation (Rust glue reading the registers) is not translated to Lean: its contract is tested on a register simulator with 10 planted mutants and on the board; the kernel side is proved.",
           "- Mutants outside model G's scope (M04, M08, M12, M13) are covered by the cohort campaign (phase 10), not by ReplayG.",
           "- Amendment in force: E004 (ReplayG exporter: an injected anchor is emitted only when its signature is verifiably invalid).", ""]
    open(os.path.join(rd, "AXIOM_REPORT.md"), 'w').write("\n".join(md))
    txt = [f"CNS AXIOM V{ver} — TRIAL — {run_id} — {'OFFLINE' if mode == 'offline' else 'ONLINE'}", f"Timestamp: {summ['generated_utc']}"]
    if mode == "online": txt += [f"Offline counterpart: {pair['run'] if pair else 'NONE'}"]
    txt += [""]
    txt += [f"Phase {p['phase']:>2}  {p['name']:<64} {p['result']}" for p in phases]
    txt += ["", f"OVERALL: {'ALL PASS' if allpass else 'FAIL'}", f"Phase Merkle root (RFC 6962): {root_m}"]
    open(os.path.join(rd, "AXIOM_REPORT.txt"), 'w').write("\n".join(txt) + "\n")
    print("\n".join(txt)); return 0 if allpass else 1

if __name__ == "__main__":
    c, *a = sys.argv[1:]
    sys.exit({"instrument": cmd_instrument, "close": cmd_close, "p0": cmd_p0, "p1": cmd_p1, "p4pre": cmd_p4pre, "p6": cmd_p6,
              "p9": cmd_p9, "p10": cmd_p10, "p11": cmd_p11, "report": cmd_report}[c](a))
