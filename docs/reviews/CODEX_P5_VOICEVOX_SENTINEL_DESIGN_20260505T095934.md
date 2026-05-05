§1. sentinel signal file の最小 design

推奨は `public/narration.ready.json`。`watchStaticFile()` は `/public` 配下のファイル名を監視対象にする API なので、Studio 側は `watchStaticFile('narration.ready.json', cb)` で固定監視できる（Remotion docs: https://www.remotion.dev/docs/watchstaticfile）。`public/narration/ready.json` でも動く可能性はあるが、`getStaticFiles()` docs は Linux の subdirectory change watch に Node.js 条件を明記しているため、root 配置のほうが保守的（Remotion docs: https://www.remotion.dev/docs/getstaticfiles）。

format は空 file ではなく、最小 JSON:

```json
{
  "schemaVersion": 1,
  "status": "ready",
  "chunkCount": 3,
  "totalFrames": 1234,
  "generatedAtMs": 1760000000000
}
```

Studio runtime は中身を必須 read しない。`watchStaticFile()` callback が受け取る `StaticFile | null` の `lastModified` / `sizeInBytes` を signal key に使えるため、JSON は外部 watcher / test / 人間確認用に寄せる（Remotion docs: https://www.remotion.dev/docs/getstaticfiles）。

write order は現行順序を壊さず、最後に sentinel を足す:

`cleanup_stale_all()` で旧 sentinel 削除 → chunks → `chunk_meta.json` → `narrationData.ts` → `narration.wav` → `narration.ready.json`

現行は chunks を `atomic_write_bytes()` で置き、`write_narration_data()` が `chunk_meta.json` と `narrationData.ts` を atomic write し、その後 `concat_wavs_atomic()` で `narration.wav` を作る構造（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:571), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:338), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:378), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:638)）。sentinel は「publish 完了」の signal なので `narration.wav` 成功後だけ書く。

§2. watchStaticFile + invalidateNarrationMode との相互作用

既存 API は維持する。`useNarrationMode(): NarrationMode` の返り値と呼び出し側は変えず、hook 内に sentinel watcher を追加するだけにする。現行 hook は `watchStaticFile()` callback で `invalidateNarrationMode()` と `setMode(getNarrationMode())` を呼ぶ構造（[useNarrationMode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/useNarrationMode.ts:40)）。`MainVideo` は hook を 1 箇所で呼び、`NarrationAudioWithMode` に mode を渡して watcher 二重登録を避けているため、この構成は維持する（[MainVideo.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/MainVideo.tsx:22), [NarrationAudio.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/NarrationAudio.tsx:16)）。

dedup は 2 層で足す。まず sentinel callback は `StaticFile` が `null` の削除 event を ready signal として扱わない。次に `lastModified:sizeInBytes` を `useRef` に保持し、同一 signal key は no-op にする。legacy/chunk/sentinel の複数 event が近接する問題は、`scheduleUpdate()` を 1 個に集約し、pending 中の callback はまとめて 1 回の `invalidateNarrationMode()` にする。

重要 caveat: sentinel watcher だけでは `narrationData.ts` の static import 更新を完全保証しない。hook は `narrationData` を module import しており、effect deps は空（[useNarrationMode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/useNarrationMode.ts:3), [useNarrationMode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/useNarrationMode.ts:78)）。Vite docs も HMR boundary 外の import 更新伝播に制約があることを明記している（Vite docs: https://vite.dev/guide/api-hmr）。したがって P5 は「public asset 完了 signal の厳密化」であり、「TS timeline data を HMR から完全独立させる redesign」ではない。後者は `narrationData.ts` 依存を public JSON + async load へ移す別 scope。

§3. write 失敗時の rollback

sentinel writer は既存 `atomic_write_text()` を使う。現 helper は temp path に書いて `os.replace()` し、例外時に tmp を unlink する（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:108)）。Python docs は `os.replace()` 成功時の rename が atomic operation になると説明している（Python docs: https://docs.python.org/3/library/os.html#os.replace）。このため正常系では final path の partial JSON は観測されない設計にできる。

失敗契約は「ready が書けないなら publish 未完了」。`write_narration_ready()` を `concat_wavs_atomic()` 成功後の try に置き、`OSError` / JSON write 失敗 / `os.replace()` 失敗を `Exception` catch で拾う。catch では chunks unlink、`reset_narration_data_ts()`、`chunk_meta.json` unlink、`narration.wav` unlink、`narration.ready.json` unlink を行う。現行 concat rollback は `Exception` catch で chunks / `narrationData.ts` / `chunk_meta.json` を戻しているため、sentinel failure も同じ all-or-nothing contract に合わせる（[voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:633), [voicevox_narration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/voicevox_narration.py:640)）。

Studio 側の partial-state 検出は conservative にする。sentinel event が来ても、最終判定は既存 `getNarrationMode()` の「`narrationData` non-empty かつ全 chunk が `getStaticFiles()` に存在するなら chunks、なければ legacy / none」に任せる（[mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:19), [mode.ts](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/mode.ts:45)）。つまり corrupt sentinel 単独で chunks mode にはしない。

§4. 6 gate への影響予測

新規 Python test は必要。`test_timeline_integration.py` に、sentinel が `narration.wav` 成功後だけ存在すること、sentinel write 失敗時に `narration.wav` / chunks / meta / populated `narrationData.ts` が残らないこと、`cleanup_stale_all()` が stale sentinel を消すことを追加する。既存 write-order test は concat 呼び出し時点で `narrationData.ts` が populated かを検証し、concat failure rollback も検証しているため、sentinel は「concat 後」に追加すれば非干渉にできる（[test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:284), [test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:350), [test_timeline_integration.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/test_timeline_integration.py:383)）。

React test は `useNarrationMode.chunks.test.tsx` を更新する。現 test は `narration.wav + chunk count` の watcher 数を期待しているため、sentinel 追加後は `1 + chunk count + ready` に変わる（[useNarrationMode.chunks.test.tsx](/Users/rokumasuda/.claude/plugins/supermovie/template/src/Narration/useNarrationMode.chunks.test.tsx:133)）。また、`narration.ready.json` trigger で incomplete → chunks に再評価される case と、同一 signal key の duplicate trigger が余計な watcher 増殖を起こさない case を追加する。

6 gate 自体は増やさない。composite gate は worktree clean、regen verify、Python integration、optional lint、optional React test を含む設計なので、追加 test は既存 gate に乗る（[check_release_ready.sh](/Users/rokumasuda/.claude/plugins/supermovie/scripts/check_release_ready.sh:18)）。

§5. Effort 概算 + 推奨 PR scope

Effort は **M**。理由は writer 側は既存 atomic helper と rollback pattern の延長だが、React 側は watcher dedup と既存 watcher count test の更新が必要だから。P5 自体は release note でも後続候補扱いで、現行 race fix は残す前提になっている（[PHASE3_RELEASE_NOTE.md](/Users/rokumasuda/.claude/plugins/supermovie/docs/PHASE3_RELEASE_NOTE.md:113), [PHASE3_PROGRESS.md](/Users/rokumasuda/.claude/plugins/supermovie/docs/PHASE3_PROGRESS.md:127)）。

推奨 PR scope は **1 PR**。理由は implementation と tests を分けると、ready signal の write order / rollback / watcher dedup の契約が片方だけ入る中間状態を作るため。scope は `voicevox_narration.py`、`useNarrationMode.ts`、関連 Python/React tests、必要なら narration constants export まで。public JSON を runtime data source にする案は HMR 依存をより強く断てるが、async load と render path への影響が出るため、この P5 では除外する。
