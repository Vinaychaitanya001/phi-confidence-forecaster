#!/bin/bash
# The single final run on the held-out TEST split. Nothing here fits or tunes anything: the rules, settings and the
# four forecasters (model.joblib) come from train / cal. Run ONCE, after every design decision is final.
#   MC=1 scripts/run_test.sh     also run MC dropout (10 passes, ~75 min on CPU); the saved forecasters need these features
set -euo pipefail
cd "$(dirname "$0")/.."
P=.venv/bin/python
TAG=_v5
MC=${MC:-0}
mkdir -p results/logs
echo "== 1. detector on test (model pass + rules)"
$P -m deidconf.detect --split test 2>&1 | grep -v Warning | tail -1
if [ "$MC" = "1" ]; then
  echo "== 1b. MC dropout on test"
  $P -m deidconf.mcdropout --split test --passes 10 > results/logs/mcdropout_test.log 2>&1
  grep -v Warning results/logs/mcdropout_test.log | tail -1
fi
echo "== 2. evaluate (live rules + current label map, same settings as cal)"
$P -m deidconf.evaluate --split test --rules baseline --model redecode --tag "" 2>&1 | grep -v Warning | grep "rules+model " | sed 's/^/baseline (shipped repo rules, run live): /' || true
$P -m deidconf.evaluate --split test --rules live --model redecode --tag $TAG 2>&1 | grep -v Warning | tail -5
echo "== 3. features"
$P -m deidconf.features --split test --eval-tag $TAG --system rules+model 2>&1 | grep -v Warning | tail -2
echo "== 4. apply the forecasters fitted on cal"
for t in y_is_phi y_cat_ok y_exact; do
  $P -m deidconf.confidence --features results/features/test$TAG.rules+model.csv --target $t \
     --apply results/confidence/cal$TAG.rules+model.$t/model.joblib --run test$TAG.rules+model.$t 2>&1 | grep -v Warning | grep -E "^(raw_softmax|raw_score|gbdt:all)"
done
echo "== 5. near misses with the forecaster fitted on cal"
$P -m deidconf.nearmiss --split test --eval-tag $TAG --apply results/nearmiss/cal$TAG/model.joblib 2>&1 | grep -v Warning | grep -E "candidates in|^(raw_mass|all) |note level"
echo "== 6. robustness + report"
$P -m deidconf.robustness --split test --eval-tag $TAG 2>&1 | grep -v Warning | tail -1
$P -m deidconf.report --split test --eval-tag $TAG --baseline-tag "" 2>&1 | tail -1
echo "done: results/RESULTS_test$TAG.md"
