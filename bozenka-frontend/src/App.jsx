// Standart elements for any page
import JoyHeader from './components/Header.jsx';
import Footer from './components/Footer.jsx';


// Pages for routing
import HomePage from "./routes/Homepage.jsx"; 
import CommunitiesSearch from './routes/Communities.jsx';
import LoginPage from './routes/Login.jsx';
import Community from './routes/Community.jsx';
import RegisterPage from './routes/Register.jsx';
import Page404 from './routes/404.jsx';
import {
  DashboardHomepage, 
  DashboardBuildCommunity,
  DashboardControlCommunity,
  DashboardLayout } from './routes/Dashboard.jsx';

// Other imports
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import '@fontsource/inter';


/**
* App component
* Base function, defines the application.
* @returns {JSX.Element} - The rendered application.
*/
function App() {
 return (
   <div>
     <JoyHeader />
     <Routes>
       <Route path="/" element={<HomePage />} />
       <Route path="/communities" element={<CommunitiesSearch />} />
       <Route path='/community' element={<Community />} />
       <Route path='/login' element={<LoginPage />} />
       <Route path='/register' element={<RegisterPage />} />
       
      {/* Dashboard routes */}
      <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<DashboardHomepage />} />
          <Route path='build' element={<DashboardBuildCommunity />} />
          <Route path='communities' element={<DashboardControlCommunity />} />
          <Route path="*" element={<Page404 />}/>
      </Route>
      <Route path="*" element={<Page404/>}/>
     </Routes>
     <Footer/>
   </div>
 );
}


export default App;