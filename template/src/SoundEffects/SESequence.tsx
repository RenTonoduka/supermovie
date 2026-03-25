import { Audio, Sequence, staticFile } from 'remotion';
import { seData } from './seData';

export const SESequence: React.FC = () => {
  return (
    <>
      {seData.map((se) => (
        <Sequence key={se.id} from={se.startFrame} durationInFrames={90}>
          <Audio
            src={staticFile(`se/${se.file}`)}
            volume={se.volume ?? 1}
          />
        </Sequence>
      ))}
    </>
  );
};
