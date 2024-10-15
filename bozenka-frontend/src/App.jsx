// Standart elements for any page
import JoyHeader from './components/Header.jsx';
import Footer from './components/Footer.jsx';

// Pages for routing
import HomePage from "./routes/Homepage.jsx"; 
import CommunitiesSearch from './routes/Communities.jsx';
import LoginPage from './routes/Login.jsx';
import Community from './routes/Community.jsx';
import RegisterPage from './routes/Register.jsx';
import AreaChart from './components/GrowthChart.jsx';

// Other imports
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import '@fontsource/inter';


function App() {
  /*
    Base fuction, defines the application.;
  */
  return (
    <div>
      <JoyHeader />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/communities" element={<CommunitiesSearch />} />
        <Route path='/community' element={<Community />} />
        <Route path='/login' element={<LoginPage />} />
        <Route path='/register' element={<RegisterPage />} />
        <Route path='/test' element={<AreaChart/>} />
      </Routes>
      <Footer/>
      {/* Rest of your content */}
    </div>
  );
}

export default App;