import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Page1Entry from './pages/Page1Entry'
import Page2Training from './pages/Page2Training'
import Page3Comparison from './pages/Page3Comparison'
import Page35Review from './pages/Page35Review'
import Page4Scoring from './pages/Page4Scoring'
import Page5Cognitive from './pages/Page5Cognitive'
import Page6Payment from './pages/Page6Payment'

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Page1Entry />} />
        <Route path="/train" element={<Page2Training />} />
        <Route path="/compare" element={<Page3Comparison />} />
        <Route path="/error-review" element={<Page35Review />} />
        <Route path="/score" element={<Page4Scoring />} />
        <Route path="/cognitive" element={<Page5Cognitive />} />
        <Route path="/pay" element={<Page6Payment />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
