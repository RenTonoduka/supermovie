# SuperMovie Observability Contract

本 doc は SuperMovie pipeline の observability に関する最小規約を固定する。Codex 19:50 consult verdict (Tech 改善 Medium #3、`/Users/rokumasuda/0_Daily-Workspace/handoff_2026-05-05_1741_supermovie-phase3-pr-cycle.md:60`) に準拠した doc-only PR scope。script migration / env var rename / provider price 記載 / external SaaS 前提は本 doc では扱わない。

## Scope And Non-Goals

### Scope (本 doc が固定する)
- status JSON emission の canonical な仕様 (`--json-log` 動作、stdout/stderr 区別、common fields)
- log redaction の対象種別と適用 rule
- cost telemetry の単位・rate env var convention・missing rate 時の挙動
- migration policy (current v0 → future v1)
- test 要件 (regression 防止)

### Non-Goals (本 doc では扱わない)
- script 実装 (本 PR は doc-only、migration commit は別 PR)
- env var rename (既存 `SUPERMOVIE_RATE_INPUT_PER_MTOK` 系の alias 化以上は別 PR)
- provider 個別 pricing 記載 (network 制約下で未検証、`docs/api-operation-guard` 系参照)
- external SaaS / GCP / credential 前提 (本 PR では required にしない)
- distributed tracing / metrics export 実装 (`run_id` reservation のみ、実装は別 PR)

## Current Surface

実装済の observability surface (Bash 実測 2026-05-05 19:36):

| script | --json-log | cost guard | dry-run | redaction status |
|---|---|---|---|---|
| `generate_slide_plan.py` | ✓ ([:168](../template/scripts/generate_slide_plan.py)) | ✓ ([:161,297](../template/scripts/generate_slide_plan.py)) | ✓ ([:159](../template/scripts/generate_slide_plan.py)) | partial (API key OK / transcript text not redacted) |
| `voicevox_narration.py` | ✓ ([:523](../template/scripts/voicevox_narration.py)) | minimal | — | partial (chunk text in human log) |
| `preflight_video.py` | — | — | — | — (input path 出力あり) |
| `timeline.py` | — | — | — | — |
| `visual_smoke.py` | summary JSON artifact ([:365](../template/scripts/visual_smoke.py)) | — | — | — |
| `build_slide_data.py` | — | — | — | raw title/telop text on stdout |
| `build_telop_data.py` | — | — | — | raw title/telop text on stdout |
| `compare_telop_split.py` | — | — | — | — |

`--json-log` 実装は `generate_slide_plan.py:168` と `voicevox_narration.py:523` の 2 箇所が canonical pattern、他 5 script は本 doc 確定後に別 PR で migration 候補。

## Status JSON Contract

### Emission Contract

- `--json-log` flag が指定された時のみ、stdout の **末尾 1 行** に純 JSON (改行で終端) を emit する。
- human-readable stdout (進捗 message 等) は `--json-log` 有無に関係なく維持する。
- error / warning は `stderr` に出す。`--json-log` 時も stderr 経路は変えない。
- 1 invocation 1 emission を default。multiple emission を採る場合は `schema_version` で variant を区別する。

既存の test 契約 (`test_timeline_integration.py:1167`, `:2173`) は本 contract の正規化版。

### Common Fields (schema v1)

```json
{
  "schema_version": 1,
  "script": "generate_slide_plan",
  "status": "ok|skipped|error|dry_run",
  "ok": true,
  "exit_code": 0,
  "category": "phase3-slide|phase3-narration|...",
  "duration_ms": 1234,
  "counts": { "<domain-specific>": 0 },
  "artifacts": [
    { "path": "<relative or redacted absolute>", "kind": "json|wav|ts|png|..." }
  ],
  "cost": {
    "currency": "USD",
    "estimate": 0.0,
    "rate_source": "env:SUPERMOVIE_RATE_..._PER_MTOK"
  },
  "redaction": {
    "applied_rules": ["api_key", "abs_path", "user_content"],
    "version": 1
  },
  "run_id": "<reserved for future tracing, optional, UUID v4>",
  "parent_run_id": "<optional>",
  "step_id": "<optional>"
}
```

### Status Naming (canonical 値)

| value | 用途 |
|---|---|
| `ok` | 成功完走 |
| `skipped` | precondition 不在等で no-op skip (e.g., engine 不在で voicevox skip、idempotent skip) |
| `error` | 異常終了 (exit_code ≠ 0)、`category` で詳細 |
| `dry_run` | API call せず estimate のみ出力 |

### Stdout And Stderr

| stream | 内容 |
|---|---|
| stdout (human) | 進捗 message、preflight output、最終 summary。`--json-log` 時も維持。 |
| stdout (json tail) | 末尾 1 行に schema v1 JSON。`--json-log` 指定時のみ。 |
| stderr | error message、warning、stack trace、retry attempt。 |

`--json-log` consumer は **stdout の末尾 1 行のみを JSON parse** する想定。途中の human message を JSON parse させない。

### Script Coverage Matrix

current state (v0) は `generate_slide_plan.py` / `voicevox_narration.py` が `status` / `exit_code` を出す最小形 ([generate_slide_plan.py:177](../template/scripts/generate_slide_plan.py), [voicevox_narration.py:533](../template/scripts/voicevox_narration.py))。本 doc 確定後の future v1 で全 script に schema v1 を適用する別 PR を予定。

## Log Redaction Contract

### Sensitive Classes

| class | 例 | source |
|---|---|---|
| secret | `ANTHROPIC_API_KEY` 等 API key、token、credential | env / config / argv |
| user_content | transcript text、segments、telop raw text、prompt body | input file / API request body |
| abs_path | `/Users/<name>/...` machine-local 絶対 path | argparse / sys.argv / output file path |
| provider_response_body | LLM API の response 全文 | network response |

### Redaction Rules

- secret: 値の最後 4 文字以外をマスク (`sk-...XXXX`)。env name / config key 名は出して可。
- user_content: human stdout には出してよい。json tail には raw 出さず `length` / `hash` のみ。
- abs_path: human stdout には出してよい。json tail / artifact path は repo root 相対 path に変換、外部に出る log は `~` 展開後に `<HOME>` placeholder。
- provider_response_body: human stdout に出さず stderr のみ、かつ secret-bearing header は事前 strip。

### Path Policy

artifact `path` field は repo root or project root からの **相対 path** で記録する。絶対 path は `redaction.applied_rules` に `abs_path` を含めて redacted variant を記録するか、user invocation context で必要なら明示 opt-in flag (`--unsafe-keep-abs-path`) を script 側に追加 (本 doc は規約のみ、実装は別 PR)。

### User Content Policy

`build_slide_data.py:388` / `build_telop_data.py:453` のように raw title/telop text を human stdout に出している script は、json tail には length / hash のみを出す形に migration する (別 PR)。raw text を残す合理理由 (debug 等) がある場合は flag 化して default off。

## Cost Telemetry Contract

### Cost JSON Shape

```json
{
  "currency": "USD",
  "estimate": 0.0,
  "rate_source": "env:SUPERMOVIE_RATE_<PROVIDER>_<DIR>_USD_PER_MTOK",
  "rate_input_usd_per_mtok": 1.0,
  "rate_output_usd_per_mtok": 5.0,
  "tokens_input": 1234,
  "tokens_output": 567,
  "rate_missing": false
}
```

### Rate Env Var Convention

- v1 canonical: `SUPERMOVIE_RATE_<PROVIDER>_<DIRECTION>_USD_PER_MTOK`
  - 例: `SUPERMOVIE_RATE_ANTHROPIC_INPUT_USD_PER_MTOK`、`SUPERMOVIE_RATE_GEMINI_OUTPUT_USD_PER_MTOK`
- v0 (既存): `SUPERMOVIE_RATE_INPUT_PER_MTOK` / `SUPERMOVIE_RATE_OUTPUT_PER_MTOK` ([generate_slide_plan.py:161](../template/scripts/generate_slide_plan.py))
  - v1 が未設定で v0 が設定されている場合の alias 動作を future PR で定義 (本 doc は規約のみ)。

### Provider Notes

| provider | unit | rate kind |
|---|---|---|
| Anthropic API (slide plan) | $/MTok input + $/MTok output | text generation、env 必須 |
| Gemini API (image gen) | $/image | image generation、別 env 系 (本 doc 後の別 PR で固定) |
| VOICEVOX (narration) | local engine、cost なし ([voicevox_narration.py:66](../template/scripts/voicevox_narration.py)) | telemetry 対象外 |
| Kling / 他 (将来) | provider 個別 | 別 doc 化 |

### Missing Rate Behavior

- rate env が未設定: `cost.estimate = null`、`cost.rate_missing = true`、`status = ok` (cost 不明は error 扱いしない)。
- rate が設定されているが invalid (NaN / 負値等): `status = error`、`category = "rate-invalid"`、exit_code 非 0。
- `nan/inf` ガードは既存 `generate_slide_plan.py:120` 系の挙動を canonical とする。

## Migration Policy

| state | criteria |
|---|---|
| v0 (current) | `status` / `exit_code` を出す最小 status JSON、redaction なし、cost rate env は v0 名 |
| v1 (target) | schema_version=1、common fields 全埋め (null OK)、redaction 適用、rate env は v1 名 + v0 alias |

migration steps (別 PR scope):
1. v0 → v1 schema 互換 helper を `template/scripts/_observability.py` に追加 (新規 file)。
2. 既存 2 script (`generate_slide_plan.py` / `voicevox_narration.py`) を helper 経由に refactor。
3. 残 5 script (`preflight_video.py` / `timeline.py` / `visual_smoke.py` / `build_*` / `compare_telop_split.py`) を v1 化。
4. test_timeline_integration.py に regression test 追加。

## Test Requirements

- `test_timeline_integration.py` に redaction regression test (sensitive class 4 種が json tail に raw で出ないこと) を追加 (別 PR)。
- 各 script の `--json-log` を CI で smoke test (parse + schema_version 確認)。
- cost telemetry の missing rate behavior を test fixture で確認。

## Open Questions

- `run_id` / `parent_run_id` / `step_id` の発行責任 (script 内自動 vs 呼出側経由)。本 doc では reservation のみ、決定は別 PR。
- artifact path の repo-root vs project-root 解釈 (現行 supermovie pipeline は `<PROJECT>` ベース、release repo は repo root ベース)。
- redaction `version` の bump policy (schema_version とは独立、redaction rule 変更時のみ bump)。
- VOICEVOX 以外の local engine が増えた場合の cost 取り扱い (cost null vs 削除)。
