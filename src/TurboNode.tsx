import React, { memo, type ReactNode } from 'react';
import { FiCloud } from 'react-icons/fi';
 
import { 
  Handle, 
  Position, 
  type Node, 
  type NodeProps,
} from '@xyflow/react';
 
export type TurboNodeData = {
  title: string;
  icon?: ReactNode;
  subline?: string;
};
 
export default memo((props: NodeProps<Node<TurboNodeData>>) => {
  const { 
    data, 
    selected,
    isConnectable,
    selectable = true,
    deletable = true,
    draggable = true,
    ...rest 
  } = props;
  
  return (
    <div {...rest}>
      <div className={`cloud gradient ${selected ? 'selected' : ''}`}>
        <div>
          <FiCloud />
        </div>
      </div>
      <div className="wrapper gradient">
        <div className="inner">
          <div className="body">
            {data.icon && <div className="icon">{data.icon}</div>}
            <div>
              <div className="title">{data.title}</div>
              {data.subline && <div className="subline">{data.subline}</div>}
            </div>
          </div>
          <Handle 
            type="target" 
            position={Position.Left}
            isConnectable={isConnectable}
          />
          <Handle 
            type="source" 
            position={Position.Right}
            isConnectable={isConnectable}
          />
        </div>
      </div>
    </div>
  );
});