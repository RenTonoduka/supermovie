# SuperMovie API Operation Guard

paid / remote API を呼ぶ全 skill / script に共通する operation guard 規約。本 doc は **規約のみ**、provider 固定値 / retry 定数 / endpoint URL は一切書かない。

> **設計出典**: Codex consult `b6kk55pue` (2026-05-05 17:14) acceptance gate 通過の verdict 準拠。

## 適用範囲

- 既存: Gemini image API (`skills/supermovie-image-gen` で `GEMINI_API_KEY` 経由)
- prior art: Anthropic API (Phase 3 release branch HEAD `8310a4c` の `template/scripts/generate_slide_plan.py`、main にはまだ存在しない release scope)
- 将来 paid / remote API (Phase 4-6 候補、`docs/roadmap/FUTURE_FEATURES_REQUIREMENTS_v0.md` §4)
- VOICEVOX local は本 guard 適用外 (network 不要)、ただし future remote VOICEVOX は対象

## 9 必須 element

### 1. API key preflight

- 必要な env (例: `GEMINI_API_KEY` / `ANTHROPIC_API_KEY`) 不在で paid API call しない
- key 値は **表示・ログ化しない**、存在チェックのみ
- 不在時は `status: api_key_skipped` で skip status を返す

### 2. Dry-run first

- 全 paid operation は dry-run mode を持つ
- dry-run は API call せず、request plan + estimate JSON を返す
- 形式: `--dry-run` flag、または default dry-run + `--apply` で実行
- dry-run で出した plan を Roku (またはユーザー) が確認、**明示承認後**に本実行

### 3. No hardcoded price

- provider の price / rate を doc / script に固定値で書かない
- CLI arg / env / 公式 docs 再確認で供給する
- 月予算 / 単価は `[Roku decision required: ...]` placeholder で残す

### 4. Cost estimate formula

status JSON に以下を含める:
- `estimated_input_tokens`
- `estimated_output_tokens_upper_bound`
- `estimation_method` (例: "ceil(prompt_chars/4)" などの計算式)
- optional `rate_input_per_1m_tokens`, `rate_output_per_1m_tokens` (Roku / env 経由で供給)
- optional `estimated_cost_usd` (rate 提供時のみ計算、なければ "rate_unset" で省略)

### 5. Status JSON schema (minimum fields)

| field | description |
|---|---|
| `status` | success / api_key_skipped / rate_limited / api_http_error / cost_guard_arg_invalid / inputs_missing / llm_json_invalid / dry_run_estimate / 等 |
| `exit_code` | 0 / 1 / 4 / 9 等 (具体値は script 側仕様) |
| `api_called` | bool (dry-run なら false) |
| `provider` | "gemini" / "anthropic" / etc |
| `operation` | 例 "image_generation" / "slide_plan" |
| `model` | provider model name (空文字 OK) |
| error / retry fields | 該当時 (`error_code`, `retry_after`, `http_status` 等) |

### 6. Rate-limit handling

- 429 / equivalent HTTP status は `status: rate_limited` で分離
- `retry_after` header があれば status JSON に含める (sec / iso8601)
- **doc 内に固定 sleep 秒数 / 固定 retry 回数を書かない**、script 側で env / config 化
- 自動 retry を doc で規約化しない (script 設計次第)

### 7. Roku decision placeholders

以下は本 doc 内で実値を埋めず、placeholder で残す:
- `[Roku decision required: monthly budget USD per provider]`
- `[Roku decision required: legal review for new API (commercial terms / privacy / data retention)]`
- `[Roku decision required: moral / 著作権 / 本人許諾 review (deepfake / voice cloning / 第三者 IP 利用 等)]`
- `[Roku decision required: publish / deploy timing for the operation result]`

実値 (実 USD 数値、実承認日、実 deploy 日) はここに書かず、別場所 (project-config / handoff / Roku の external decision log) で管理する。

### 8. API key / endpoint URL

- 本 doc は API key 文字列 / executable endpoint URL を規約として書かない
- 個別 skill / script doc に委譲 (例: `skills/supermovie-image-gen/SKILL.md` で `GEMINI_API_KEY` 言及)

### 9. public_reference author guard

- 上流 repo (例: `RenTonoduka/supermovie`) の author / maintainer は **License 表記以外で** stakeholder / reviewer / approver / Roku blocker 扱いしない
- 案件に応じて Roku が判断 (例: 上流取り込みを目指す or fork で完結)
- `[Roku decision required: upstream contribution strategy (fork-only / upstream PR / archive)]`

## Prior art (Phase 3 release branch、main 未到達)

本 doc の 9 element は Phase 3 release branch の `template/scripts/generate_slide_plan.py` (release HEAD `8310a4c` 時点、main にはまだ存在しない) で先行実装されている。同 script の pattern:
- `--dry-run` で API 呼ばず estimate JSON
- `--max-tokens` / `--max-input-words` / `--max-input-segments` (env override 可)
- 429 を `rate_limited` で分離、`retry_after` 拾い
- `emit_json(status, exit_code, **extra)` helper

新 skill / script を起こす時は、上記 pattern を参照して同じ shape で実装する。

## 移行対象 (別 PR scope)

`skills/supermovie-image-gen/SKILL.md` の現行記述で固定 wait / retry が含まれる箇所は、本 guard に従って env / config 化する (別 PR で対応)。

---

**本 doc 自身の更新ルール**:
- 新 element / pattern を追加する時は Codex consult acceptance gate を通す
- 価格 / retry 定数 / endpoint URL を doc に固定値で書かない
- public_reference 作者を stakeholder 扱いする変更は invariant 違反、reject 対象

(本 doc は Codex consult `b6kk55pue` 2026-05-05 17:14 verdict 準拠の最小規約 doc。)
