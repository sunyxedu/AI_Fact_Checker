import { BrowserRouter, Routes, Route } from 'react-router-dom';
import FlowComponent from './FlowComponent';
import NestedFlowComponent from './NestedFlowComponent';

import { useNavigate } from 'react-router-dom';

const exampleJson = {
  nodes: [1,2,3,4,5,6,7,8,9],
  node_names: ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
  severity: [1,2,3,4,5,1,2,3,1],
  edges: [[1,2], [2,3], [1,3], [1,5],[1,6],[6,7],[7,8],[8,9]]
};

const exampleJson2 = {
  nodes: [1,2,3,4,5,6,7,8,9,10,11,12],
  node_names: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
  severity: [1,2,3,4,5,1,2,3,1,2,3,1],
  edges: [[1,2], [2,3], [1,3], [1,5],[1,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,12]]
};

interface NestedNodePageProps {
  data: typeof exampleJson2;
}

function NestedNodePage({ data }: NestedNodePageProps) {
  const navigate = useNavigate();
  
  return (
    <div>
      <button onClick={() => navigate(-1)}>Back</button>
      <NestedFlowComponent data={data} />
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FlowComponent data={exampleJson} />} />
        <Route 
          path="/node/:nodeId" 
          element={<NestedNodePage data={exampleJson2} />} 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
