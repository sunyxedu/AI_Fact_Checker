import React, { memo } from 'react';
import { Handle, Position, type NodeProps } from 'reactflow';

export default memo(({ data }: NodeProps) => {
  return (
    <div className="node-glow-container">
      <div className="node-glow"></div>
      <div className="node-content">
        <div className="node-label">{data.label}</div>
        <Handle type="target" position={Position.Left} />
        <Handle type="source" position={Position.Right} />
      </div>
    </div>
  );
});
