import './App.css';
import { BrowserRouter as Router, Route, Routes, Outlet } from 'react-router-dom'
import { AuthProvider } from './AuthContext';
import Home from './components/Home/Home';
import Login from './components/Login/Login';
import ChatRoom from './components/ChatRoom/ChatRoom';
import SignUp from './components/SingUp/SignUp';
import PrivateRoute from './PrivateRoute';

function App() {
  return (
    <AuthProvider>
      <Router >
        <div className="App">
          <Routes className="App">
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/chat/*" element={<PrivateRoute />}>
              <Route path=":room_name/" element={<ChatRoom />} />
            </Route>
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;