"""Step 3b: MC-dropout passes of the existing model (paper 1's uncertainty signal). No training.

    python -m deidconf.mcdropout --split cal --passes 10        (resumable; ~N x single-pass time)

Dropout layers are switched to train mode (everything else stays frozen and in eval mode); the model is run N times
with different seeds; per word we keep the mean and standard deviation of the full softmax vector and the per-pass
arg-max label. Written to results/mcdropout/<split>/<note_id>.npz:
    P_mean (n_words, n_tags) float16, P_std (n_words, n_tags) float16, argmax (N, n_words) int16,
    spans (n_words, 2) int32 (identical to results/detect/<split>/probs/<note_id>.npz)
"""
from __future__ import annotations

import argparse
import json
import time

import numpy as np

from deidconf import PROJECT_ROOT
from deidconf.data import read_jsonl
from deidconf.detect import adapted_configs, score_words_full


def enable_dropout(model) -> list[str]:
    import torch
    on = []
    for name, m in model.named_modules():
        if isinstance(m, torch.nn.Dropout):
            m.train()
            on.append(f"{name}(p={m.p})")
    return on


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="cal")
    ap.add_argument("--passes", type=int, default=10)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--out", default="results/mcdropout")
    a = ap.parse_args(argv)

    import torch
    from deid.detectors.hf_detector import build_detector

    det_cfg, models_cfg, labels_cfg = adapted_configs()
    model = build_detector(models_cfg["selected"], models_cfg, labels_cfg, det_cfg, deployment=False, threads=a.threads)
    if model.backend != "torch":
        raise SystemExit("MC dropout needs the torch backend")
    layers = enable_dropout(model.model)
    out = PROJECT_ROOT / a.out / a.split
    out.mkdir(parents=True, exist_ok=True)
    (out / "meta.json").write_text(json.dumps({"passes": a.passes, "seed": a.seed, "dropout_layers": layers,
                                                "hidden_dropout_prob": getattr(model.model.config, "hidden_dropout_prob", None),
                                                "attention_dropout": getattr(model.model.config, "attention_probs_dropout_prob", None)},
                                               indent=1), encoding="utf-8")
    print(f"dropout enabled in {len(layers)} layers, e.g. {layers[:3]}", flush=True)

    notes = read_jsonl(PROJECT_ROOT / f"data/meddeid/{a.split}.jsonl")
    if a.limit:
        notes = notes[:a.limit]
    todo = [n for n in notes if not (out / f"{n['note_id']}.npz").exists()]
    print(f"{a.split}: {len(notes)} notes, {len(notes) - len(todo)} done, {len(todo)} to run x {a.passes} passes", flush=True)
    t_start = time.perf_counter()
    for i, n in enumerate(todo, 1):
        Ps = []
        spans = None
        for k in range(a.passes):
            torch.manual_seed(a.seed * 100_003 + k)
            sw = score_words_full(model, n["text"])
            if sw is None:
                break
            spans, P = sw
            Ps.append(P)
        if not Ps:
            np.savez_compressed(out / f"{n['note_id']}.npz", P_mean=np.zeros((0, len(model.tags)), np.float16),
                                P_std=np.zeros((0, len(model.tags)), np.float16), argmax=np.zeros((a.passes, 0), np.int16),
                                spans=np.zeros((0, 2), np.int32))
            continue
        S = np.stack(Ps)                                        # (N, words, tags)
        np.savez_compressed(out / f"{n['note_id']}.npz", P_mean=S.mean(0).astype(np.float16),
                            P_std=S.std(0).astype(np.float16), argmax=S.argmax(-1).astype(np.int16),
                            spans=np.asarray(spans, dtype=np.int32).reshape(-1, 2))
        if i % 25 == 0 or i == len(todo):
            el = time.perf_counter() - t_start
            print(f"  {i}/{len(todo)}  {el / i:.2f} s/note  eta {(len(todo) - i) * el / i / 60:.0f} min", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
