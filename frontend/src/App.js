import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Home from './components/Home/Home';
import Login from './components/Login/Login';
import ChatRoom from './components/ChatRoom/ChatRoom';
import SignUp from './components/SingUp/SignUp';


function App() {
  return (
    <Router>
      <div className="App">
        <Routes className="App">
          <Route path="/" element={<Home />} />
          <Route path="/chat/:room_name" element={<ChatRoom />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;