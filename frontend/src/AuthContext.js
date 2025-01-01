import React, { createContext, useEffect, useState } from 'react';
import {jwtDecode} from 'jwt-decode'

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [userId, setUserId] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('accessToken');

        if (token) {
            const decodeToken = jwtDecode(token);
            setUserId(decodeToken.user_id);
        }
    }, []);

    return (
        <AuthContext.Provider value={{ userId, setUserId }}>
            {children}
        </AuthContext.Provider>
    );
};
