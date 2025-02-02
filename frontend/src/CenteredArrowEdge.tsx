import { BaseEdge, getStraightPath } from 'reactflow';

export default function CenteredArrowEdge({
  sourceX,
  sourceY,
  targetX,
  targetY,
  markerEnd,
  style,
}: any) {
  const [edgePath] = getStraightPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
  });

  // Calculate exact midpoint
  const midX = (sourceX + targetX) / 2;
  const midY = (sourceY + targetY) / 2;

  // Calculate angle in radians
  const angleRad = Math.atan2(targetY - sourceY, targetX - sourceX);
  const angleDeg = angleRad * (180 / Math.PI);

  // Arrow dimensions
  const arrowSize = 20;
  const arrowCenter = arrowSize / 2;

  return (
    <>
      <BaseEdge path={edgePath} style={style} />
      <g transform={`translate(${midX}, ${midY})`}>
        <path
          d={`M-${arrowCenter},-${arrowCenter/2} L${arrowCenter},0 -${arrowCenter},${arrowCenter/2} Z`}
          fill="#fff"
          stroke="#fff"
          strokeWidth={1}
          transform={`rotate(${angleDeg})`}
        />
      </g>
    </>
  );
} 