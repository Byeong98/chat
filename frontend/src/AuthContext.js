import React, { createContext, useEffect, useState } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [userName, setUserName] = useState(null);

    useEffect(() => {
        const savedUserName = localStorage.getItem('CurrentUser');
        if (savedUserName) {
            setUserName(savedUserName);
        }
    }, []);

    return (
        <AuthContext.Provider value={{ userName, setUserName }}>
            {children}
        </AuthContext.Provider>
    );
};
