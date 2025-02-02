import React from 'react';
import ReactFlow, { Controls, Background, Node, Edge } from 'reactflow';
import 'reactflow/dist/style.css';
import { forceSimulation, forceManyBody, forceLink, forceCollide, forceX, forceY } from 'd3-force';
import { useNavigate } from 'react-router-dom';
import CustomNode from './CustomNode';

const severityDict: { [key: number]: string } = {
  1: "#cc8f00", // Darker yellow-orange
  2: "#cc6e00", // Darker orange
  3: "#b3540d", // Darker reddish-orange
  4: "#992e0d", // Darker red
  5: "#7a1509"  // Darker deep red
};

interface FlowComponentProps {
  data: {
    nodes: number[];
    node_names: string[];
    severity: number[];
    edges: number[][];
  };
  title: {
    header: string;
  };
}

const defaultProps = {
  title: { title: "Default Title" }
};

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
        width: 120,
        height: 120,
        borderRadius: '15%',
        fontSize: '1rem',
        border: `3px solid ${severityDict[jsonData.severity[index] as keyof typeof severityDict]}`,
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.2)'
      }
    }
  }));

  const links = jsonData.edges.map(([source, target]) => ({
    source: source.toString(),
    target: target.toString()
  }));

  forceSimulation(nodes as any)
    .force('charge', forceManyBody().strength(-1500))
    .force('link', forceLink(links).id(d => (d as any).id).distance(300))
    .force('collide', forceCollide().radius(100).strength(1))
    .force('x', forceX().strength(0.02))
    .force('y', forceY().strength(0.02))
    .stop()
    .tick(400);

  return nodes.map(node => ({
    ...node,
    position: { x: node.x || 0, y: node.y || 0 } // IGNORE THIS ERROR ITS GOOD
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

export default function FlowComponent({ 
  data, 
  title
}: FlowComponentProps) {
  const navigate = useNavigate();

  const handleNodeClick = (event: React.MouseEvent, node: Node) => {
    navigate(`/node/${node.id}`);
  };

  const initialNodes = createNodes(data);
  const initialEdges = createEdges(data);

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#1a1a1a' }}>
      <h1 id="header-component">{title.header}</h1>
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
    </div>
  );
} 