import React from 'react';
import ReactFlow, { Controls, Background, Node, Edge } from 'reactflow';
import 'reactflow/dist/style.css';
import { forceSimulation, forceManyBody, forceLink, forceCollide, forceX, forceY } from 'd3-force';
import { useNavigate } from 'react-router-dom';
import CustomNode from './CustomNode';


const severityDict: { [key: number]: string } = {
  1: "#ffb700",
  2: "#ffa325",
  3: "#f77d19",
  4: "#f74919",
  5: "#ae1e0f"
};

interface FlowComponentProps {
  data: {
    nodes: number[];
    node_names: string[];
    severity: number[];
    edges: number[][];
  };
}

// Add node types configuration
const nodeTypes = {
  custom: CustomNode,
};

const createNodes = (jsonData: FlowComponentProps['data']): Node[] => {
  const nodes = jsonData.nodes.map((nodeId, index) => ({
    id: nodeId.toString(),
    type: 'custom',
    position: { x: 0, y: 0 },
    data: {
      label: jsonData.node_names[index],
      style: {
        backgroundColor: '#000',
        color: 'white',
        width: index === 0 ? 150 : 120,
        height: index === 0 ? 150 : 120,
        borderRadius:  '15%',
        fontSize: index === 0 ? '1.5rem' : '1rem',
        border: `3px solid ${severityDict[jsonData.severity[index] as keyof typeof severityDict]}`,
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.2)'
      }
    }
  }));

  const links = jsonData.edges.map(([source, target]) => ({
    source: source.toString(),
    target: target.toString()
  }));

  // Create force simulation
  forceSimulation(nodes as any)
    .force('charge', forceManyBody().strength(-1500)) //this is the level of repulsion between nodes
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

const createEdges = (jsonData: FlowComponentProps['data']): Edge[] => {
  return jsonData.edges.map(([source, target], index) => ({
    id: `edge-${source}-${target}-${index}`,
    source: source.toString(),
    target: target.toString(),
    style: {
      stroke: '#fff',
      strokeWidth: 2,
      strokeOpacity: 0.8
    },
    animated: true
  }));
};

export default function NestedFlowComponent({ data }: FlowComponentProps) {
  const navigate = useNavigate();

  const handleNodeClick = (event: React.MouseEvent, node: Node) => {
    navigate(`subnode/${node.id}`);
  };

  const initialNodes = createNodes(data);
  const initialEdges = createEdges(data);

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#1a1a1a' }}>
      <ReactFlow 
        nodes={initialNodes}
        edges={initialEdges}
        nodeTypes={nodeTypes}
        onNodeClick={handleNodeClick}
        fitView
      >
        <Background color="#404040" gap={24} />
        <Controls />
      </ReactFlow>
      <button onClick={() => navigate(-1)}>Back</button>
    </div>
  );
} 