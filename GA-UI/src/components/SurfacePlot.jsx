import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

const Rastrigin3D = () => {
  const [point, setPoint] = useState({ x: 0, y: 0, z: 0 });
  const [camera, setCamera] = useState({
    projection: { type: 'perspective' },
  });

  // Rastrigin function definition
  const rastrigin = (x, y, A = 10) => {
    return (
      A * 2 +
      (x ** 2 - A * Math.cos(2 * Math.PI * x)) +
      (y ** 2 - A * Math.cos(2 * Math.PI * y))
    );
  };

  // Generate grid data for the Rastrigin function
  const gridSize = 50;
  const x = Array.from({ length: gridSize }, (_, i) => (i - gridSize / 2) * 0.5);
  const y = Array.from({ length: gridSize }, (_, i) => (i - gridSize / 2) * 0.5);
  const z = x.map((xi) => y.map((yi) => rastrigin(xi, yi)));

  useEffect(() => {
    // Animate the point over the Rastrigin function
    let t = 0; // Time variable
    const interval = setInterval(() => {
      t += 0.1; // Increment time
      const newX = 10 * Math.sin(t); // Circular motion on X
      const newY = 10 * Math.cos(t); // Circular motion on Y
      const newZ = rastrigin(newX, newY); // Z from Rastrigin function
      setPoint({ x: newX, y: newY, z: newZ });

      // Reset the loop every 2π (~6.28 seconds)
      if (t >= 2 * Math.PI) {
        t = 0;
      }
    }, 100); // Update every 100ms (10 frames per second)
    return () => clearInterval(interval);
  }, []);

  // Preserve camera state when the user interacts
  const handleRelayout = (event) => {
    if (event['scene.camera']) {
      setCamera(event['scene.camera']);
    }
  };

  return (
    <Plot
      data={[
        {
          z: z,
          x: x,
          y: y,
          type: 'surface',
          colorscale: 'Viridis',
        },
        {
          x: [point.x],
          y: [point.y],
          z: [point.z],
          mode: 'markers',
          type: 'scatter3d',
          marker: { size: 8, color: 'red' },
          name: 'Moving Point',
        },
      ]}
      layout={{
        title: 'Rastrigin Function with Moving Point',
        scene: {
          xaxis: { title: 'X' },
          yaxis: { title: 'Y' },
          zaxis: { title: 'Z' },
          camera: camera, // Apply the preserved camera state
        },
        dragmode: 'orbit',
      }}
      config={{
        scrollZoom: true,
      }}
      onRelayout={handleRelayout} // Capture camera changes
      style={{ width: '100%', height: '100%' }}
    />
  );
};

export default Rastrigin3D;
