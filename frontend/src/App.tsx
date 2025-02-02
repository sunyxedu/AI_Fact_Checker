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
    text: string[];
    dates: number[];
    edges: number[][];
  };
}

interface DoubleNestedNodePageProps {
  data: {
    nodes: number[];
    nodename: string[];
    severities: number[];
    urls: string[];
    edge: number[][];
    
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
    names: [],
    severities: [],
    truthieness: [],
    edges: []
  });

  const [jsonLvl2, setJsonLvl2] = useState({
    nodes: [],
    text: [],
    dates: [],
    edges: []
  });

  const [jsonLvl3, setJsonLvl3] = useState({
    nodes: [],
    nodename: [],
    severities: [],
    urls: [],
    edge: []
    
  });

  const [titleData, setTitleData] = useState({
    header: "",
    videoUrl: ""
  });

  const location = useLocation();
  
  const fetchJsonLvl1 = async () => {
    try {
      const response = await fetch('http://localhost:5000/misinformation/');
      const data = await response.json();
      setJsonLvl1(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchJsonLvl2 = async (node_id: number) => {
    try {
      const response = await fetch('http://localhost:5000/statement' +  "/"+String(node_id));// + "/{node_id}
      const data = await response.json();
      setJsonLvl2({
        ...data,
        node_name: data.node_name || ""
      });
    } catch (error) {
      console.error('Error fetching level 2 data:', error);
    }
  };

  const fetchJsonLvl3 = async (node_id: number) => {
    try {
      const response = await fetch('http://localhost:5000/provinence' +  "/"+String(node_id));
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
    fetchJsonLvl2(0);
    fetchJsonLvl3(0);
    fetchTitleData();
  }, [location.pathname]);

  return (
    <AnimatePresence mode='wait'>
      <Routes location={location} key={location.pathname}>
        <Route 
          path=  "/" 
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
          path="/misinformation/:nodeId" 
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
          path="/misinformation/:nodeId/subnode/:subnodeId" 
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
        <Route path="/video_url" element={<div>{titleData.videoUrl}</div>} />
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
