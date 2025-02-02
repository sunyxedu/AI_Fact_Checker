import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import FlowComponent from './FlowComponent';
import NestedFlowComponent from './NestedFlowComponent';
import DoubleNestedFlowComponent from './DoubleNestedFlowComponent';
import { useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import React from 'react';




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
  node_name: [""],
  edges: [[1,2], [1,3], [1,4], [1,5], [1,6]]
};

const exampleJson3 = {
  nodes: [1,2,3,4,5],
  node_names: ["link", "link", "link", "link", "link"],
  severity: [1,2,3,4,5],
  edges: [[1,2], [2,3], [3,4], [4,5]],
  node_name: [""],
  links: ["link", "link", "link", "link", "link"]
};

const exampleTitle = {header: "Youtube Video: Trump Inauguration"}

interface NestedNodePageProps {
  data: {
    nodes: number[];
    node_names: string[];
    severity: number[];
    edges: number[][];
    node_name: string;
  };
}

interface DoubleNestedNodePageProps {
  data: {
    nodes: number[];
    node_names: string[];
    severity: number[];
    edges: number[][];
    node_name: string;
    links: string[];
  };
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

function DoubleNestedNodePage({ data }: DoubleNestedNodePageProps) {
  const navigate = useNavigate();
  
  return (
    <div>
      <button onClick={() => navigate(-1)}>Back</button>
      <DoubleNestedFlowComponent data={data} />
    </div>
  );
}

function AnimatedRoutes() {
  const [jsonLvl1, setJsonLvl1] = useState({
    nodes: [],
    node_names: [],
    severity: [],
    edges: []
  });

  const [jsonLvl2, setJsonLvl2] = useState({
    nodes: [],
    node_names: [],
    severity: [],
    edges: [],
    node_name: []
  });

  const [jsonLvl3, setJsonLvl3] = useState({
    nodes: [],
    node_names: [],
    severity: [],
    edges: [],
    node_name: [],
    link: []
  });

  const [titleData, setTitleData] = useState({
    header: "",
    videoUrl: ""
  });

  const location = useLocation();
  
  const fetchJsonLvl1 = async () => {
    try {
      const response = await fetch('http://localhost:5000/node_lvl_1');
      const data = await response.json();
      setJsonLvl1(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchJsonLvl2 = async () => {
    try {
      const response = await fetch('http://localhost:5000/node_lvl_2');
      const data = await response.json();
      setJsonLvl2({
        ...data,
        node_name: data.node_name || ""
      });
    } catch (error) {
      console.error('Error fetching level 2 data:', error);
    }
  };

  const fetchJsonLvl3 = async () => {
    try {
      const response = await fetch('http://localhost:5000/node_lvl_3');
      const data = await response.json();
      setJsonLvl3(data);
    } catch (error) {
      console.error('Error fetching level 3 data:', error);
    }
  };

  const fetchTitleData = async () => {
    try {
      const [titleRes, urlRes] = await Promise.all([
        fetch('http://localhost:5000/lvl_2_title'),
        fetch('http://localhost:5000/video_url')
      ]);
      
      const titleData = await titleRes.json();
      const urlData = await urlRes.json();
      
      setTitleData({
        header: titleData.header,
        videoUrl: urlData.url
      });
    } catch (error) {
      console.error('Error fetching title data:', error);
    }
  };

  useEffect(() => {
    fetchJsonLvl1();
    fetchJsonLvl2();
    fetchJsonLvl3();
    fetchTitleData();
  }, [location.pathname]);

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
              <FlowComponent data={jsonLvl1} title={titleData}/>
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
              <NestedNodePage data={jsonLvl2} />
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
              <DoubleNestedNodePage data={jsonLvl3} />
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
