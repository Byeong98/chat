import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const PrivateRoute = () => {
    const { userName } = useContext(AuthContext);
    console.log(userName, 1)
    
    return userName ? <Outlet /> : <Navigate to="/login" replace />;
};

export default PrivateRoute;
