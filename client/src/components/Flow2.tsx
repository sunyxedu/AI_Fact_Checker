import React, { useCallback, useState } from "react";
import {
  ReactFlow,
  addEdge,
  useEdgesState,
  useNodesState,
  Node,
  Edge,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

// ✅ Define Node Class (Wrapper)
class MindMapNode {
  id: string;
  label: string;
  position: { x: number; y: number };

  constructor(id: string, label: string, x: number, y: number) {
    this.id = id;
    this.label = label;
    this.position = { x, y };
  }

  getNode(): Node {
    return {
      id: this.id,
      data: { label: this.label },
      position: this.position,
      type: "custom",
    };
  }
}

// ✅ Initial Nodes
const initialNodes: Node[] = [
  new MindMapNode("1", "Start Node", 150, 100).getNode(),
];

const initialEdges: Edge[] = [];

const Flow2 = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [nodeCount, setNodeCount] = useState(2); // Track new node IDs

  // ✅ Click Handler: Console log and create a new node
  const onNodeClick = useCallback(
    (_event: React.MouseEvent, node: Node) => {
      console.log("Clicked Node:", node.data.label);

      // Create new node with "hi" concatenation
      const newNode = new MindMapNode(
        nodeCount.toString(),
        `${node.data.label} hi`,
        node.position.x + 200, // Adjust X position
        node.position.y + 100 // Adjust Y position
      ).getNode();

      // Create new edge
      const newEdge: Edge = { id: `e${node.id}-${newNode.id}`, source: node.id, target: newNode.id, markerEnd: "none" };

      // Update State
      setNodes((nds) => [...nds, newNode]);
      setEdges((eds) => [...eds, newEdge]);
      setNodeCount((count) => count + 1); // Increment for next node
    },
    [setNodes, setEdges, nodeCount]
  );

  return (
    <div className="w-screen h-screen bg-gray-100">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        fitView
      />
    </div>
  );
};

export default Flow2;
