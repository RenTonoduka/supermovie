**結論**
推奨は **cost guard 単独 PR** です。`generate_slide_plan.py` は現状 `max_tokens=4096` 固定、`words[:200]`、segments 全量投入、HTTPError 一律 `return 4` です（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:103), [generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:128), [generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:146)）。P3 `--json-log` 統合は別 PR 推奨です。

**1. Final Spec**

| CLI / env | default | type / range | spec |
|---|---:|---|---|
| `--max-tokens` / `SUPERMOVIE_MAX_TOKENS` | `4096` | int, `1..16384` | CLI > env > default。`body["max_tokens"]` に入れる。`16384` は API 上限ではなく local safety cap。既存 default は維持（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:130), Roku発言: "default 4096 維持"） |
| `--max-input-words` / `SUPERMOVIE_MAX_INPUT_WORDS` | `200` | int, `>=1` | `words[:N]` に使う。prompt 文言の「最大 200 word」も `{N}` 化する（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:61), [generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:103)） |
| `--max-input-segments` / `SUPERMOVIE_MAX_INPUT_SEGMENTS` | unset | int, `>=1` | 追加推奨。未指定なら segments 全量で既存互換、指定時だけ `segments[:N]`。segments は現状全量なので long input source になり得る（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:107), Roku発言: "segments full は long input source"） |
| `--dry-run` | false | flag | API を呼ばず、prompt 生成後に JSON を stdout へ出して `0`。API key は不要。入力ファイル欠落は既存同様 `3`（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:80), [generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:86)） |
| `--rate-input` / `SUPERMOVIE_RATE_INPUT_PER_MTOK` | unset | decimal, `>=0` | USD/MTok。両 rate がある時だけ cost 推定を出す。価格 hardcode はしない（Roku発言: "価格 hardcode 禁止"） |
| `--rate-output` / `SUPERMOVIE_RATE_OUTPUT_PER_MTOK` | unset | decimal, `>=0` | USD/MTok。同上 |

Dry-run JSON は最低限これでよいです: `status:"dry_run"`, `api_called:false`, `model`, `max_tokens`, `max_input_words`, `max_input_segments`, `words_in_prompt`, `segments_in_prompt`, `prompt_chars`, `estimated_input_tokens`, `estimated_output_tokens_upper_bound`, `estimated_cost_usd_upper_bound|null`, `rate_input_per_mtok|null`, `rate_output_per_mtok|null`, `estimation_method:"ceil(prompt_chars/4)"`。

注意点: Anthropic 公式 docs で確認できる正攻法は Token Counting API で、入力 token count は estimate 扱いです（https://platform.claude.com/docs/en/build-with-claude/token-counting）。`chars/4` はこの PR では **local heuristic** と明示すべきです（Roku発言: "prompt 文字列 chars/4"）。

**2. 実装フロー**

1. `argparse` で新 flag を追加。env 解決 helper は `resolve_int(cli, env, default, min, max)` と `resolve_decimal(cli, env)` に分ける。通常実行では API key 未設定 skip を先に維持し、dry-run 時だけ API key なしで config 解決する（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:80)）。

2. `transcript/config` 読み込み後、`words_preview` は `words[:max_input_words]`。`segments_preview` は `--max-input-segments` 指定時だけ `segments[:N]`、未指定は現状通り全量（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:96)）。

3. prompt 生成後、`--dry-run` なら body を作らず JSON 出力。`estimated_input_tokens = ceil(len(prompt) / 4)`、`estimated_output_tokens_upper_bound = max_tokens`。両 rate がある時だけ `input/1_000_000*rate_input + output/1_000_000*rate_output` を出す。Anthropic docs 上、Messages API の request size limit は 32MB なので、dry-run に `request_body_bytes_estimate` を入れるとレビューしやすいです（https://platform.claude.com/docs/en/api/errors）。

4. API 呼び出し body の `max_tokens` を `args/env/default` 解決値へ置換する（[generate_slide_plan.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/generate_slide_plan.py:128)）。

5. `HTTPError` catch で `e.code == 429` を分岐し、`retry-after = e.headers.get("retry-after")` を拾って stderr に出し `return 9`。429 以外は現行 `return 4` 維持。Anthropic docs は 429 を `rate_limit_error`、`retry-after` header を待機秒として説明しています（https://platform.claude.com/docs/en/api/errors, https://platform.claude.com/docs/en/api/rate-limits）。

補足: 現行 Anthropic docs では `max_tokens` は OTPM rate limit 計算に入らないと説明されています。したがって `--max-tokens` は rate-limit guard というより、出力 cost upper bound と validation guard です（https://platform.claude.com/docs/en/api/rate-limits）。

**3. Tests**

1. `test_generate_slide_plan_dry_run_no_api_key`: temp project、API key unset、`urlopen` は呼ばれたら fail。stdout JSON の `status=dry_run`, `api_called=false`, `estimated_*` を assert。

2. `test_generate_slide_plan_max_tokens_override`: env と CLI の precedence を mock request body で assert。既存 success mock は `urlopen(req)` を受けているので `req.data` を JSON parse できる（[test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:724)）。

3. `test_generate_slide_plan_max_tokens_cap_rejects`: `--max-tokens 16385` で parser error / SystemExit を assert（Roku発言: "例: 16384 cap"）。

4. `test_generate_slide_plan_max_input_caps_prompt`: 3 words / 3 segments を作り、`--max-input-words 2 --max-input-segments 1` で dry-run または mock request body に 3rd word / 2nd segment が入らないことを assert。

5. `test_generate_slide_plan_rate_limited_429`: 既存 HTTP error test は 429 で `return 4` を期待しているため、期待値を `9` に変更し `retry-after` header も検証（[test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:813)）。

6. `test_generate_slide_plan_api_http_error_non_429`: 500 mock を追加し、429 以外は `return 4` を維持することを assert。

**4. emit_json Scope**

P3 logging 統合は **別 PR** 推奨。`voicevox_narration.py` の `emit_json` は `--json-log` 付きで全 return path を status JSON 化する設計で、success / skip / strict path の専用 tests もあります（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:520), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:533), [test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:1550)）。`generate_slide_plan.py` に同時展開すると、skip / missing inputs / dry-run / 429 / HTTP error / invalid JSON / success 全 return path の schema test が増えます。

P3 拡張は次 PR で、1. `--json-log` 追加、2. local `emit_json(status, exit_code, **extra)` 追加、3. 全 return path を status 化、4. 既存 stdout 維持 test、の4 stepが妥当です。今回 PR は dry-run JSON と 429 status 名だけ先に揃えるのが最小です。

**5. Effort / PR Scope**

Effort は **M**。変更は主に `generate_slide_plan.py` と `test_timeline_integration.py` の mock tests で収まりますが、env precedence、dry-run、429 分岐、既存 HTTP test 更新が入ります（[test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:671), [CODEX_NEXT_PRIORITY](/Users/rokumasuda/.claude/plugins/supermovie/docs/reviews/CODEX_NEXT_PRIORITY_20260505T102232.md:10)）。

推奨 PR scope は **cost guard 単独**。P3 logging は `CODEX_NEXT_PRIORITY` でも別項目なので、同時統合すると review surface が広がります（[CODEX_NEXT_PRIORITY](/Users/rokumasuda/.claude/plugins/supermovie/docs/reviews/CODEX_NEXT_PRIORITY_20260505T102232.md:15)）。
