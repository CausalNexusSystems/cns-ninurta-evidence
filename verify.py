#!/usr/bin/env python3
"""Offline verifier for this evidence repository (standard library only).
Checks, from the published bytes alone:
  1. every published run file equals the hash committed in its run's TRIAL_MANIFEST.txt;
  2. every phase seal in summary.json is the SHA-256 of the published phase result, and the RFC 6962 Merkle root of the
     13 phase seals equals the root in summary.json and in AXIOM_REPORT.txt;
  3. the online run names its offline counterpart and the SHA-256 of that run's TRIAL_MANIFEST.txt (PAIR.txt);
  4. the closure manifest (seal 27) commits to every published run file, to amendment E005 and to the
     pre-registration manifest (seal 26);
  5. the pre-registration manifest (seal 26) commits to the trial runner published here and is dated before the runs;
  6. each .ots proof is a proof for the digest of the file next to it.
Bitcoin attestation of the .ots proofs is checked with the OpenTimestamps client:  ots verify <file>.ots
Usage:  python3 verify.py"""
import hashlib, json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); ok = True
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else "MISSING"
def say(good, msg):
    global ok; ok &= good; print(("PASS " if good else "FAIL ") + msg)
def sums(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        m = re.match(r"^([0-9a-f]{64})\s+\*?(.+?)\s*$", l)
        if m: d[m.group(2)] = m.group(1)
    return d
def merkle(leaves):
    H = lambda b: hashlib.sha256(b).digest(); nodes = [H(b"\x00" + bytes.fromhex(x)) for x in leaves]
    def mth(n):
        if len(n) == 1: return n[0]
        k = 1
        while k * 2 < len(n): k *= 2
        return H(b"\x01" + mth(n[:k]) + mth(n[k:]))
    return mth(nodes).hex()
RUNS = os.path.join(ROOT, "runs"); s27 = sums(os.path.join(ROOT, "closure", "SEAL27_MANIFEST.txt"))
s26p = os.path.join(ROOT, "preregistration", "SEAL26_MANIFEST.txt"); s26 = sums(s26p)
runs = sorted(os.listdir(RUNS)); summ = {}
for r in runs:
    d = os.path.join(RUNS, r); tm = sums(os.path.join(d, "TRIAL_MANIFEST.txt")); n = bad = 0
    for base, _, fs in os.walk(d):
        for f in fs:
            rel = os.path.relpath(os.path.join(base, f), d).replace(os.sep, "/")
            if rel.endswith(".ots") or rel in ("TRIAL_MANIFEST.txt", "SEAL_LOG.txt"): continue
            n += 1; bad += tm.get("./" + rel) != sha(os.path.join(d, rel))
    say(n > 0 and bad == 0, f"{r}: {n} published files equal their TRIAL_MANIFEST.txt commitments")
    s = json.load(open(os.path.join(d, "summary.json"), encoding="utf-8")); summ[r] = s
    seals = [p["phase_seal"] for p in s["phases"]]
    eq = all(sha(os.path.join(d, f"phase{p['phase']}", f"phase{p['phase']}_result.json")) == p["phase_seal"] for p in s["phases"])
    root = merkle(seals); txt = open(os.path.join(d, "AXIOM_REPORT.txt"), encoding="utf-8").read()
    say(eq and len(seals) == 13 and root == s["phase_merkle_root_rfc6962"] and f"Phase Merkle root (RFC 6962): {root}" in txt,
        f"{r}: 13 phase seals = SHA-256 of the phase results; recomputed Merkle root {root[:16]}... = summary = report ({s['mode']}, {s['overall']})")
    nf = 0; bf = 0
    for base, _, fs in os.walk(d):
        for f in fs:
            rel = os.path.relpath(os.path.join(base, f), d).replace(os.sep, "/")
            if rel.endswith(".ots"): continue
            nf += 1; bf += s27.get(f"trial_v3/runs/{r}/{rel}") != sha(os.path.join(d, rel))
    say(bf == 0, f"{r}: {nf} files committed in the closure manifest (seal 27)")
for r, s in summ.items():
    if s["mode"] == "online" and s["overall"] != "ALL PASS":
        print(f"INFO {r}: failed online run kept as a record (amendment E005); it pairs with nothing")
    elif s["mode"] == "online":
        p = open(os.path.join(RUNS, r, "PAIR.txt"), encoding="utf-8").read().split()
        off = p[0] if p else ""; good = off in summ and summ[off]["mode"] == "offline" and summ[off]["overall"] == "ALL PASS" \
            and p[1] == sha(os.path.join(RUNS, off, "TRIAL_MANIFEST.txt")) and s.get("pair_offline_run", {}).get("run") == off
        say(good, f"{r}: online run paired with offline run {off} by the SHA-256 of its TRIAL_MANIFEST.txt")
e5 = [f for f in os.listdir(os.path.join(ROOT, "closure")) if f.startswith("E005")][0]
say(s27.get("00_GOVERNANCE/enmiendas/" + e5) == sha(os.path.join(ROOT, "closure", e5)), "amendment E005 committed in seal 27")
say(s27.get("00_GOVERNANCE/proofs/SEAL26_MANIFEST.txt") == sha(s26p), "seal 27 is chained to seal 26 (pre-registration)")
pre = [f for f in os.listdir(os.path.join(ROOT, "preregistration")) if not f.startswith("SEAL26")]
say(all(s26.get("trial_v3/" + f) == sha(os.path.join(ROOT, "preregistration", f)) for f in pre), f"pre-registration (seal 26) commits to the published trial runner ({len(pre)} files)")
utc = re.search(r"^utc=(\S+)", open(s26p, encoding="utf-8").read(), re.M).group(1).replace("-", "").replace(":", "")
say(all(utc < r.split("_")[-1] for r in runs), f"seal 26 dated {utc} before every run ({', '.join(r.split('_')[-1] for r in runs)})")
for base, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".ots"):
            target = os.path.join(base, f[:-4]); b = open(os.path.join(base, f), "rb").read()
            say(os.path.isfile(target) and hashlib.sha256(open(target, "rb").read()).digest() in b,
                f"{os.path.relpath(os.path.join(base, f), ROOT)} is a proof for the digest of {os.path.basename(target)}"
                + ("; Bitcoin attestation present" if bytes.fromhex("0588960d73d71901") in b else "; Bitcoin attestation PENDING (run: ots upgrade)"))
print("\nVERIFY: " + ("PASS" if ok else "FAIL") + "   (then: ots verify <file>.ots for the Bitcoin attestations)"); sys.exit(0 if ok else 1)
