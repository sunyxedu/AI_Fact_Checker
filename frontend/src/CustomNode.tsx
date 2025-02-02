import React, { memo, useRef, useEffect } from 'react';
import { Handle, Position, type NodeProps } from 'reactflow';

const scaleTextToFit = (element: HTMLElement) => {
  const container = element.parentElement;
  if (!container) return;

  let fontSize = parseFloat(getComputedStyle(element).fontSize);
  const minFontSize = 8;
  const maxFontSize = 24;
  
  while (
    (element.scrollHeight > container.clientHeight || 
     element.scrollWidth > container.clientWidth) && 
    fontSize > minFontSize
  ) {
    fontSize -= 0.5;
    element.style.fontSize = `${fontSize}px`;
  }

  while (
    (element.scrollHeight < container.clientHeight * 0.9 && 
     element.scrollWidth < container.clientWidth * 0.9) && 
    fontSize < maxFontSize
  ) {
    fontSize += 0.5;
    element.style.fontSize = `${fontSize}px`;
  }
};

export default memo(({ data }: NodeProps) => {
  const textRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (textRef.current) {
      const resizeObserver = new ResizeObserver(() => {
        textRef.current!.style.fontSize = ''; // Reset before recalculating
        scaleTextToFit(textRef.current!);
      });
      
      resizeObserver.observe(textRef.current);
      scaleTextToFit(textRef.current);
      
      return () => resizeObserver.disconnect();
    }
  }, [data.label]);

  return (
    <div className="node-glow-container">
      <div className="node-glow"></div>
      <div className="node-content" style={{ 
        ...data.style,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'Roboto, sans-serif'
      }}>
        <div 
          ref={textRef}
          className="node-label"
          style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '4px',
            transition: 'font-size 0.3s ease'
          }}
        >
          {data.label}
        </div>
        <Handle type="target" position={Position.Left} />
        <Handle type="source" position={Position.Right} />
      </div>
    </div>
  );
});
