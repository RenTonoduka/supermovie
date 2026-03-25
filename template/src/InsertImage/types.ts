export interface ImageSegment {
  id: number;
  startFrame: number;
  endFrame: number;
  file: string;
  type: 'photo' | 'infographic' | 'overlay';
  scale?: number;
}
