import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import FlowComponent from './FlowComponent';
import NestedFlowComponent from './NestedFlowComponent';
import DoubleNestedFlowComponent from './DoubleNestedFlowComponent';
import { useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';

const exampleJson = {
  nodes: [1,2,3,4,5,6,7,8,9],
  node_names: ["Mexicans", "Black People", "White People", "Asians", "Indians", "Middle Easterners", "Latin Americans", "African Americans", "Native Americans"],
  severity: [1,2,3,4,5,1,2,3,1],
  edges: []
};

const exampleJson2 = {
  nodes: [1,2,3,4,5,6],
  node_names: ["random quote bla blaasdasd asdasdasdasdasdasdasda sdasdasdasdasdasdasdasdasdasd", "random quote bla bla", "random quote bla bla", "random quote bla bla", "random quote bla bla", "random quote bla bla"],
  severity: [1,2,3,4,5,1],
  edges: [[1,2], [1,3], [1,4], [1,5], [1,6]]
};

const exampleJson3 = {
  nodes: [1,2,3,4,5],
  node_names: ["link", "link", "link", "link", "link"],
  severity: [1,2,3,4,5],
  edges: [[1,2], [2,3], [3,4], [4,5]]
};

const exampleTitle = {header: "Youtube Video: Trump Inauguration"}

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
function DoubleNestedNodePage({ data }: NestedNodePageProps) {
  const navigate = useNavigate();
  
  return (
    <div>
      <button onClick={() => navigate(-1)}>Back</button>
      <DoubleNestedFlowComponent data={data} />
    </div>
  );
}

function AnimatedRoutes() {
  const location = useLocation();
  
  return (
    <AnimatePresence mode='wait'>
      <Routes location={location} key={location.pathname}>
        <Route 
          path="/" 
          element={
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <FlowComponent data={exampleJson} title={exampleTitle}/>
            </motion.div>
          } 
        />
        <Route 
          path="/node/:nodeId" 
          element={
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <NestedNodePage data={exampleJson2} />
            </motion.div>
          } 
        />
        <Route 
          path="/node/:nodeId/subnode/:subnodeId" 
          element={
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <DoubleNestedNodePage data={exampleJson3} />
            </motion.div>
          } 
        />
      </Routes>
    </AnimatePresence>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AnimatedRoutes />
    </BrowserRouter>
  );
}

export default App;
