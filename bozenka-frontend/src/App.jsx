// Standard elements for any page
import JoyHeader from './components/Header.jsx';
import Footer from './components/Footer.jsx';

// Hooks of Bozenka
import { useAuth } from './api/contexts/AuthContext.jsx'

// Pages for routing
import HomePage from "./routes/public/Homepage.jsx"; 
import CommunitiesSearch from './routes/public/Communities.jsx';
import LoginPage from './routes/public/Login.jsx';
import Community from './routes/public/Community.jsx';
import RegisterPage from './routes/public/Register.jsx';
import Page404 from './routes/public/404.jsx';
import {
  DashboardHomepage, 
  DashboardBuildCommunity,
  DashboardControlCommunity,
  DashboardLayout, 
  DashboardControlAccount,
  DashboardCreateCommunity,
  DashboardImportCommunity
} from './routes/protected/Dashboard.jsx';

// Other imports
import { Routes, Route, Navigate } from 'react-router-dom';
import '@fontsource/inter';



const AuthorizedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated)
    return <Navigate to="/login" state={{ from: window.location.pathname }} replace />;
  return children;
}

const UnauthorizedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated)
    return <Navigate to="/dashboard" state={{ from: window.location.pathname }} replace />;
  return children;
}

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
       <Route path='/community/:id' element={<Community />} />
       
       {/* Protected unauthorized routes */}
       <Route path='/login' element={
         <UnauthorizedRoute>
           <LoginPage />
         </UnauthorizedRoute>
       } />
       <Route path='/register' element={
         <UnauthorizedRoute>
           <RegisterPage />
         </UnauthorizedRoute>
       } />
       
       {/* Protected authorized routes */}
       <Route path="/dashboard" element={
         <AuthorizedRoute>
           <DashboardLayout />
         </AuthorizedRoute>
       }>
           <Route index element={<DashboardHomepage />}/>
           <Route path='build' element={<DashboardBuildCommunity />} />
           <Route path='build/create' element={<DashboardCreateCommunity/>}/>
           <Route path='build/import' element={<DashboardImportCommunity/>}/>
           <Route path='communities' element={<DashboardControlCommunity />} />
           <Route path='account' element={<DashboardControlAccount/>}/>
           <Route path="*" element={<Page404 />}/>
       </Route>
       
       <Route path="*" element={<Page404/>}/>
     </Routes>
     <Footer/>
   </div>
 );
}

export default App;