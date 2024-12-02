import { useState } from 'react'
import SurfacePlot from './components/SurfacePlot'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <SurfacePlot />
    </>
  )
}

export default App
