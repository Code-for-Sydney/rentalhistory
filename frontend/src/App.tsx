import React from "react";
import { BrowserRouter as Router, Routes, Route, } from "react-router-dom";
import SearchPage from "./Search";
import DisplayResults from "./DisplayResults";

// App Component with Router
const App: React.FC = () => (
  <Router>
    <Routes>
      <Route path="/" element={<SearchPage />}/>
      <Route path="/results" element={<DisplayResults />} />
    </Routes>
  </Router>
);

export default App;