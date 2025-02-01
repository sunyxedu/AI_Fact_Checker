import React from 'react';
import { 
  ReactFlow,
  Background, 
  Controls, 
  Handle, 
  NodeProps, 
  Edge, 
  Node, 
  Connection,
  Position  // Import the Position enum
} from '@xyflow/react';

// Type definitions
interface CustomNodeData {
  label: string;
}

type CustomNode = Node & {
  width: number;
  height: number;
};

type HandleId = 
  | 'top-source' | 'bottom-source' | 'left-source' | 'right-source'
  | 'top-target' | 'bottom-target' | 'left-target' | 'right-target';

interface ConnectionInfo {
  source: string;
  target: string;
}

// Custom node component
const CustomNode = ({ label }: CustomNodeData) => {
  return (
    <div className="custom-node">
      {/* Adjust the Position values as needed */}
      <Handle type="source" position={Position.Top} id="top-source" />
      <Handle type="source" position={Position.Left} id="bottom-source" />
      <Handle type="source" position={Position.Bottom} id="left-source" />
      <Handle type="source" position={Position.Right} id="right-source" />
      
      <Handle type="target" position={Position.Top} id="top-target" />
      <Handle type="target" position={Position.Left} id="bottom-target" />
      <Handle type="target" position={Position.Bottom} id="left-target" />
      <Handle type="target" position={Position.Right} id="right-target" />
      
      <div>{label}</div>
    </div>
  );
};

// Helper functions
const getHandlePosition = (node: CustomNode, handleId: HandleId) => {
  // Extract the direction prefix from the handle id.
  const handleType = handleId.split('-')[0];
  const width = node.width || 200;
  const height = node.height || 100;

  switch (handleType) {
    case 'top': return { x: node.position.x + width / 2, y: node.position.y };
    case 'bottom': return { x: node.position.x + width / 2, y: node.position.y + height };
    case 'left': return { x: node.position.x, y: node.position.y + height / 2 };
    case 'right': return { x: node.position.x + width, y: node.position.y + height / 2 };
    default: throw new Error(`Invalid handle type: ${handleType}`);
  }
};

const findClosestHandles = (sourceNode: CustomNode, targetNode: CustomNode) => {
  const sourceHandles: HandleId[] = ['top-source', 'bottom-source', 'left-source', 'right-source'];
  const targetHandles: HandleId[] = ['top-target', 'bottom-target', 'left-target', 'right-target'];

  let closest = { distance: Infinity, sourceHandle: '', targetHandle: '' };

  sourceHandles.forEach(sh => {
    targetHandles.forEach(th => {
      const sp = getHandlePosition(sourceNode, sh);
      const tp = getHandlePosition(targetNode, th);
      const dx = sp.x - tp.x;
      const dy = sp.y - tp.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < closest.distance) {
        closest = { 
          sourceHandle: sh, 
          targetHandle: th, 
          distance 
        };
      }
    });
  });

  return closest;
};

const generateEdges = (nodes: CustomNode[], connections: ConnectionInfo[]): Edge[] => {
  return connections.map(conn => {
    const sourceNode = nodes.find(n => n.id === conn.source);
    const targetNode = nodes.find(n => n.id === conn.target);

    if (!sourceNode || !targetNode) {
      throw new Error('Invalid connection - missing node');
    }

    const { sourceHandle, targetHandle } = findClosestHandles(sourceNode, targetNode);

    return {
      id: `${conn.source}-${conn.target}`,
      source: conn.source,
      target: conn.target,
      sourceHandle,
      targetHandle,
      type: 'smoothstep',
      markerEnd: 'arrowclosed' as const,
    };
  });
};

// Main component
function Flow3() {
  const initialNodes: CustomNode[] = [
    { 
      id: 'A',
      position: { x: 0, y: 0 },
      data: { label: 'Node A' },
      width: 200,
      height: 100,
      type: 'custom'
    },
    {
      id: 'B',
      position: { x: 300, y: 100 },
      data: { label: 'Node B' },
      width: 200,
      height: 100,
      type: 'custom'
    },
    {
      id: 'C',
      position: { x: 600, y: -50 },
      data: { label: 'Node C' },
      width: 200,
      height: 100,
      type: 'custom'
    },
    {
      id: 'D',
      position: { x: 0, y: 200 },
      data: { label: 'Node D' },
      width: 200,
      height: 100,
      type: 'custom'
    },
    {
      id: 'E',
      position: { x: 400, y: 300 },
      data: { label: 'Node E' },
      width: 200,
      height: 100,
      type: 'custom'
    }
  ];

  const initialConnections: ConnectionInfo[] = [
    { source: 'A', target: 'B' },
    { source: 'A', target: 'C' },
    { source: 'B', target: 'D' },
    { source: 'C', target: 'E' },
    { source: 'D', target: 'E' }
  ];

  const edges = generateEdges(initialNodes, initialConnections);

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow 
        nodes={initialNodes}
        edges={edges}
        fitView
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}

export default Flow3;
