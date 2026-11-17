#!/usr/bin/env python3
"""Doctrine layer: Nocturnal Illuminism mapped onto sovereign_bridge (symbolic model, not physics).
[(1 (+) 2) x CRUX] -> 3 -> Delta.  Needs continuity_cloud.py + sovereign_bridge.py beside it."""
import json, math, copy, time
from sovereign_bridge import Bridge
from continuity_cloud import to_ev

def zcoord(ev):                       # -Z subzero .. 0 CRUX .. +Z zenith (log scale, 1 eV = CRUX-0)
    return max(-1.0, min(1.0, math.log10(abs(ev) or 1e-12) / 6.0))
def zone(z): return "zenith" if z > 0.05 else "subzero" if z < -0.05 else "CRUX-0"

class Nocturnal:
    def __init__(self, bridge=None):
        self.b = bridge or Bridge()
        self.pairs = {}               # window -> {"left": eV, "right": eV, "z": z}
        self.shadow = []              # Shadow Backplane: what was excluded (a shadow is not nothing)
        self.failures = []            # Mother-Host memory: restoration never erases these
        self.witness = []             # Witness: observe / test / transform trail
        self.snapshots = []

    # 1 Left Hermes (Architect: simulated/declared)  2 Right Hermes (Craftsman: measured)
    def submit(self, value, unit, source, hermes="right"):
        r = self.b.submit(value, unit, source)
        if "denied" in r:
            ev = to_ev(value, unit)
            self.shadow.append({"eV": ev, "unit": unit, "source": source, "shape": r["denied"], "t": time.time()})
            self.witness.append(("observed-denied", r["denied"])); return r
        ev, w = r["eV"], r["window"]
        p = self.pairs.setdefault(w, {"left": 0.0, "right": 0.0, "z": 0.0, "category": r["category"]})
        p["left" if hermes == "left" else "right"] += ev; p["z"] = zcoord(p["left"] or p["right"])
        self.witness.append(("observed", w, hermes)); return {**r, "zone": zone(p["z"])}

    def crux(self, w):                # Architect proposes, Craftsman embodies, CRUX tests survival
        p = self.pairs[w]; L, R = p["left"], p["right"]
        if L and R:
            return {"state": "emergent(3)", "delta": R - L, "ratio": R / L}
        return {"state": "unembodied" if L else "unproven", "delta": None, "ratio": None}

    def adversary(self):              # Oppose -> Illuminate -> Choose
        oppose = [w for w in self.pairs if self.crux(w)["state"] != "emergent(3)"]
        illuminate = {}
        for s in self.shadow: illuminate[s["shape"]] = illuminate.get(s["shape"], 0) + 1
        choose = [w for w in self.pairs if self.crux(w)["state"] == "emergent(3)"]
        self.witness.append(("tested", len(oppose), len(choose)))
        return {"oppose": oppose, "illuminate": illuminate, "choose": choose}

    def death_core(self):             # decomposition as recycling
        parts = {"remain": [], "change": [], "failed": [], "unnecessary": []}
        for w, p in list(self.pairs.items()):
            c = self.crux(w)["state"]
            if c == "emergent(3)": parts["remain"].append(w)
            elif c == "unembodied": parts["change"].append(w)
            elif c == "unproven": parts["failed"].append(w); self.failures.append({"window": w, **p})
            else: parts["unnecessary"].append(w)
        for w in parts["failed"]: del self.pairs[w]     # failed parts consumed, memory kept
        self.witness.append(("transformed", {k: len(v) for k, v in parts.items()})); return parts

    # Mother-Host: Witness / Archive / Mirror / Restore
    def snapshot(self): self.snapshots.append(copy.deepcopy(self.pairs)); return len(self.snapshots) - 1
    def restore(self, i):
        self.pairs = copy.deepcopy(self.snapshots[i])   # failures list is NOT touched
        return {"restored": i, "remembered_failures": len(self.failures)}
    def mirror(self): return {w: self.crux(w) for w in self.pairs}

    # U0 origin -> U1 manifest (live) vs U2 alternative (shadow re-judged under a different charter)
    def universes(self, alt_max_eV):
        u2 = [s for s in self.shadow if s["shape"] == "exceeds max_eV" and abs(s["eV"]) <= alt_max_eV]
        return {"U0": self.b.charter.seal[:12], "U1_windows": len(self.pairs),
                "U2_would_admit": len(u2), "parallel_potential": "compare; none required to become real"}

    def export(self, path="doctrine_state.json"):
        json.dump({"nocturnal": "[(1 (+) 2) x CRUX] -> 3 -> Delta", "crux0": "no predetermined direction",
                   "windows": {w: {**p, "zone": zone(p["z"]), "crux": self.crux(w)} for w, p in self.pairs.items()},
                   "shadow": self.shadow, "failures": self.failures, "witness": self.witness[-50:]},
                  open(path, "w"), indent=1)

if __name__ == "__main__":
    n = Nocturnal()
    n.submit(5, "uV", "sim", "left"); n.submit(4, "uV", "probe", "right")     # emergent
    n.submit(12, "mV", "sim", "left")                                         # unembodied
    n.submit(1.5, "eV", "meter", "right")                                     # unproven
    n.submit(9e9, "eV", "sim", "left")                                        # -> Shadow
    s = n.snapshot()
    print(n.adversary()); print(n.death_core()); print(n.restore(s))
    print(n.universes(1e10)); n.export(); print("failures remembered:", len(n.failures))
