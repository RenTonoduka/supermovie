# SuperMovie Debug Guide

ローカル SuperMovie project の troubleshooting guide。生成済み Remotion project root を `<PROJECT>` と表記し、machine-local path (`/Users/...` 等) は本 doc に書かない。

> **設計出典**: Codex consult `bhe6pcn37` (2026-05-05 17:22) acceptance gate 通過の verdict 準拠。

## 検証コマンド (前提)

```bash
cd <PROJECT>
npm run dev    # Remotion Studio 起動 (preview 確認)
npm run lint   # eslint + tsc (静的検査)
```

## 1. 最初の確認順 (workflow 進度)

正規フロー (`CLAUDE.md` 参照):

```
/supermovie-init → transcribe → transcript-fix → cut → subtitles → image-gen → se → npm run dev
```

どこまで生成済みかを以下で確認:

| step | 生成物 | 確認 |
|---|---|---|
| init | `<PROJECT>/project-config.json` | exists? |
| transcribe | `<PROJECT>/transcript.json` | exists + `words[]` 入ってる? |
| transcript-fix | `<PROJECT>/transcript_fixed.json` | exists + 差分あり? |
| cut | `<PROJECT>/src/cutData.ts` | export 配列が空でない? |
| subtitles | `<PROJECT>/src/テロップテンプレート/telopData.ts` + `<PROJECT>/src/Title/titleData.ts` | export 配列が空でない? |
| image-gen | `<PROJECT>/src/InsertImage/insertImageData.ts` + `<PROJECT>/public/images/generated/*.png` | exists? |
| se | `<PROJECT>/src/SoundEffects/seData.ts` | export 配列が空でない? |

## 2. API key missing

| key | 用途 | 確認方法 |
|---|---|---|
| `GEMINI_API_KEY` | 画像生成 (image-gen skill) | env で存在のみ確認、値は表示・log 化しない |
| AssemblyAI key | transcribe skill の話者分離 mode のみ | env で存在のみ確認、必要時のみ |

注意:
- `.env` / key file を commit しない (`.gitignore` で除外済)
- key 値を log / プレビュー画面に表示しない

## 3. image-gen が動かない

確認順 (上から):

1. `<PROJECT>/src/テロップテンプレート/telopData.ts` が空でない (subtitles skill が回ったか)
2. `<PROJECT>/src/Title/titleData.ts` が空でない
3. `<PROJECT>/project-config.json` の `format` / `resolution` が正しい
4. `GEMINI_API_KEY` env が設定済み (cost guard / dry-run / status JSON 規約は別 PR で追加予定の API operation guard doc 参照、本 PR では env 存在のみ確認)
5. 生成物 `<PROJECT>/public/images/generated/*.png` + `<PROJECT>/src/InsertImage/insertImageData.ts` の存在

## 4. 画像が表示されない (生成済みなのに preview に出ない)

- `insertImageData.ts` の `file` が `<PROJECT>/public/images/<file>` に実存するか
- Remotion `<InsertImage>` は `staticFile("images/${segment.file}")` で読む
- file 名 typo / path mismatch を確認

## 5. SE が鳴らない

確認順:

1. `<PROJECT>/public/se/` に音源 file が存在
2. `<PROJECT>/src/SoundEffects/seData.ts` の `seData[i].file` が `<PROJECT>/public/se/<file>` に実存
3. Remotion `<SESequence>` は `staticFile("se/${se.file}")` で読む
4. SE 素材の準備は `SUPERMOVIE_SE_SOURCE_DIR` env 経由が推奨 (safe rsync wrapper script は別 PR で追加予定、本 PR では env 概念のみ言及)

## 6. asset missing 全般

| asset | path |
|---|---|
| base video | `<PROJECT>/public/main.mp4` (または `videoConfig.ts` の `VIDEO_FILE`) |
| BGM | `<PROJECT>/public/BGM/bgm.mp3` |
| SE | `<PROJECT>/public/se/<file>.mp3` |
| 挿入画像 (手動) | `<PROJECT>/public/images/<file>.png` |
| 挿入画像 (AI 生成) | `<PROJECT>/public/images/generated/<file>.png` |

不在の場合: asset gate (Phase 3 release branch 側 prior art、main 未到達) で render は続行可能だが、preview / 最終 render 結果に影響。具体実装は Phase 3 release branch (上流 PR) 参照。

## 7. 症状 → 確認 path → 解決策

| 症状 | 確認 path | 解決策 |
|---|---|---|
| `GEMINI_API_KEY` 未設定 | env (存在のみ確認) | `export GEMINI_API_KEY=...` or 画像なしで続行 |
| `telopData` 空 | `<PROJECT>/src/テロップテンプレート/telopData.ts` | `/supermovie-subtitles` 再実行 |
| SE 素材不足 | `<PROJECT>/public/se/` + `seData.ts` の整合 | 素材追加 (`SUPERMOVIE_SE_SOURCE_DIR` env 経由が推奨、safe rsync wrapper は別 PR 予定) or `seData.ts` 修正 |
| 画像 file 不在 | `<PROJECT>/public/images/generated/` | `/supermovie-image-gen` 再実行 (cost guard 通過後、API operation guard doc は別 PR で追加予定) |
| transcript 空 | `<PROJECT>/transcript.json` | `/supermovie-transcribe` 再実行 |
| Studio 起動失敗 | `node_modules/.bin/remotion` 存在 | `npm install` 再実行 |

## 8. 連絡先 / サポート方針

本 SuperMovie repo は **public_reference** (`RenTonoduka/supermovie`) の再現実装。**upstream author を debug 質問先 / サポート連絡先 / approver 扱いしない**。

質問の解決経路:
- Roku 自身の internal project memory store (本 doc に絶対 path は書かない、Roku machine 固有の場所)
- Codex consult (本 doc + 別 PR で追加予定の API operation guard doc 等の規約 doc)
- 公式 Remotion docs (`https://www.remotion.dev/`)
- 公式 Gemini API docs (`https://ai.google.dev/`)
- 内部の Roku + Codex consult cycle

---

**本 doc 自身の更新ルール**:
- 新症状追加は Codex consult acceptance gate を通す
- machine-local path (`/Users/...`) を doc に固定値で書かない
- API key 値 / 個人 credential を doc に書かない
- 解決時間 / 件数 / 価格の根拠なき見積もりを書かない
- public_reference 作者を connect / contact 対象として書かない (invariant 違反、reject 対象)

(本 doc は Codex consult `bhe6pcn37` 2026-05-05 17:22 verdict 準拠の最小 debug guide。)
