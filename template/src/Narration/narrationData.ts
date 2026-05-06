/**
 * Phase 3-H: voicevox_narration.py が all-or-nothing で書き換える placeholder。
 * 空 array の時は NarrationAudio が legacy 単一 narration.wav 経路に fallback する。
 */
import type { NarrationSegment } from './types';

export const narrationData: NarrationSegment[] = [];
