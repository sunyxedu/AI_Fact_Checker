import React, { useState, useCallback, useEffect } from 'react';
import ReactFlow, { Controls, Background, Node, Edge, applyNodeChanges } from 'reactflow';
import 'reactflow/dist/style.css';
import { forceSimulation, forceManyBody, forceLink, forceCollide, forceX, forceY } from 'd3-force';
import { useNavigate } from 'react-router-dom';
import CustomNode from './CustomNode';
import CenteredArrowEdge from './CenteredArrowEdge';


const severityDict: { [key: number]: string } = {
  1: "#ffb700",
  2: "#ffa325",
  3: "#f77d19",
  4: "#f74919",
  5: "#ae1e0f"
};

interface DoubleNestedFlowComponentProps {
  data: {
    nodes: number[];
    nodename: string[];
    severities: number[];
    urls: string[];
    edge: number[][];
  };
}

// Add node types configuration
const nodeTypes = {
  custom: CustomNode,
};

// Add edge types configuration
const edgeTypes = {
  centeredArrow: CenteredArrowEdge,
};

const createNodes = (jsonData: DoubleNestedFlowComponentProps['data']): Node[] => {
  const nodes = jsonData.nodes.map((subnodeId, index) => ({
    id: subnodeId.toString(),
    type: 'custom',
    position: { x: 0, y: 0 },
    data: {
      label: jsonData.nodename[index],
      url: jsonData.urls?.[index] || '',
      style: {
        backgroundColor: '#000',
        color: 'white',
        width: 120,
        height: 120,
        borderRadius: '15%',
        fontSize: '1rem',
        border: `3px solid ${severityDict[jsonData.severities[index] as keyof typeof severityDict]}`,
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.2)'
      }
    }
  }));

  const links = (jsonData.edge || []).map(([source, target]) => ({
    source: source.toString(),
    target: target.toString()
  }));

  // Create force simulation
  forceSimulation(nodes as any)
    .force('charge', forceManyBody().strength(-15000)) //this is the level of repulsion between nodes
    .force('link', forceLink(links).id(d => (d as any).id).distance(300))
    .force('collide', forceCollide().radius(100).strength(1)) //this makes it so that each node acts as a body of mass to prevent intersections
    .force('x', forceX().strength(0.02))
    .force('y', forceY().strength(0.02))
    .stop()
    .tick(400);

  return nodes.map(node => ({
    ...node,
    position: { x: node.x || 0, y: node.y || 0 }
  }));
};

const createEdges = (jsonData: DoubleNestedFlowComponentProps['data']): Edge[] => {
  return (jsonData.edge || []).map(([source, target], index) => ({
    id: `edge-${source}-${target}-${index}`,
    source: source.toString(),
    target: target.toString(),
    sourceHandle: 'center',
    targetHandle: 'center',
    type: 'centeredArrow',
    style: {
      stroke: '#fff',
      strokeWidth: 2,
      strokeOpacity: 0.8
    },
    animated: true
  }));
};

export default function DoubleNestedFlowComponent({ data }: DoubleNestedFlowComponentProps) {
  const navigate = useNavigate();
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  
  useEffect(() => {
    if (data) {
      setNodes(createNodes(data));
      setEdges(createEdges(data));
    }
  }, [data]);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  const handleNodeClick = (event: React.MouseEvent, node: Node) => {
    // Get URL from node data using the node index
    const nodeIndex = data.nodes.indexOf(Number(node.id));
    if (nodeIndex !== -1 && data.urls?.[nodeIndex]) {
      window.open(data.urls[nodeIndex], '_blank');
    }
  };

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#1a1a1a' }}>
      <ReactFlow 
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        onNodesChange={onNodesChange}
        nodesDraggable={true}
        onNodeClick={handleNodeClick}
        fitView
      >
        <Background color="#404040" gap={44} size={4} />
        <Controls />
      </ReactFlow>
    </div>
  );
} 