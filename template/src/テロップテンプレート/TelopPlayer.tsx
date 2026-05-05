import React, { useMemo } from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { Telop } from './Telop';
import { telopData } from './telopData';
import {
  telopTemplateRegistry,
  type SubtitleData,
  type SubtitleItem,
  type TelopTemplateId,
} from './telopTemplateRegistry';
import type { TelopSegment } from './telopTypes';

/**
 * registry render 経由で動かすかどうかは segment.templateId の有無で判断する。
 * - templateId が指定されている: registry の Component を SubtitleData 形式で呼び出す
 * - 指定なし: 既存 Telop.tsx (legacy template={1..6} 分岐) で描画
 *
 * registry Component は subtitleData に複数 SubtitleItem を含めることができるが、
 * TelopPlayer は時刻同期で 1 segment ずつ描画する設計なので、毎 frame で
 * `current` の SubtitleItem 1 件を含む subtitleData を生成して渡す。
 */
function segmentToSubtitleItem(segment: TelopSegment, fps: number): SubtitleItem {
  const startSec = segment.startFrame / fps;
  const endSec = segment.endFrame / fps;
  const lines = segment.text.split('\n');
  return {
    text: segment.text,
    lines,
    start: startSec,
    end: endSec,
    startFrame: segment.startFrame,
    endFrame: segment.endFrame,
  };
}

export const TelopPlayer: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const current = useMemo(
    () => telopData.find((s) => frame >= s.startFrame && frame < s.endFrame),
    [frame],
  );

  if (!current) {
    return <AbsoluteFill />;
  }

  // registry 経路 (新)
  const tplId = (current as TelopSegment).templateId as TelopTemplateId | undefined;
  if (tplId && telopTemplateRegistry[tplId]) {
    const Entry = telopTemplateRegistry[tplId];
    const subtitleData: SubtitleData = {
      fps,
      subtitles: [segmentToSubtitleItem(current, fps)],
    };
    const Component = Entry.Component;
    return (
      <AbsoluteFill>
        <Component subtitleData={subtitleData} />
      </AbsoluteFill>
    );
  }

  // legacy 経路 (旧 Telop.tsx)
  return (
    <AbsoluteFill>
      <Telop segment={current} />
    </AbsoluteFill>
  );
};
