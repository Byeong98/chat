import React, { useState, useEffect } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const PrivateRoute = () => {
    const userName = localStorage.getItem('CurrentUser');
    
    return userName ? <Outlet /> : <Navigate to="/login" replace />;
};

export default PrivateRoute;
