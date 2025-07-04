import './App.css';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import Home from './components/Home/Home';
import Login from './components/Login/Login';
import ChatRoom from './components/ChatRoom/ChatRoom';
import SignUp from './components/SignUp/SignUp';
import PrivateRoute from './PrivateRoute';
import {AuthProvider} from './AuthContext';

function App() {
  return (
      <Router >
        <AuthProvider>
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
        </AuthProvider>
      </Router>
  );
}

export default App;