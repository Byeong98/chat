import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Login.module.css'
import apiClient from '../../apiClient'
import { AuthContext } from '../../AuthContext';
import { jwtDecode } from 'jwt-decode';

const Login = () => {
    const navigate = useNavigate();
    const { setUserId } = useContext(AuthContext)

    const [data, setData] = useState({
        email: '',
        password: ''
    })

    //로그인 api 요청
    const handleLogin = async () => {
        try {
            const response = await apiClient.post(
                '/api/login/',
                {
                    email: data.email,
                    password: data.password
                }
            );
            const {access, refresh} = response.data            
            localStorage.setItem('accessToken', access);
            localStorage.setItem('refreshToken', refresh);
            
            const decodeToken = jwtDecode(access);
            setUserId(decodeToken.user_id);
            
            navigate('/');
        } catch (error) {
            console.log('error', error);
        }
    }

    //input 입력갑 저장
    const handleCange = (name, value) => {
        setData({ ...data, [name]: value })
    }

    return (
        <div className={styles.login_container}>
            <div className={styles.chat_title}>
                <h2>로그인</h2>
            </div>
            <div className={styles.login_input_container}>
                <div className={styles.input_group}>
                    <label htmlFor="email">이메일</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        placeholder="이메일 입력"
                        value={data.email}
                        onChange={e => handleCange('email', e.target.value)}
                        required
                    />
                </div>
                <div className={styles.input_group}>
                    <label htmlFor="password">비밀번호</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={data.password}
                        onChange={e => handleCange('password', e.target.value)}
                        placeholder="비밀번호 입력"
                        required
                    />
                </div>
                <input type="button" 
                        className={styles.login_button} 
                        value='로그인'
                        onClick={handleLogin}/>
            </div>
            <div className={styles.signup_container}>
                <hr />
                <input
                    className={styles.login_button}
                    type='button'
                    value='회원가입'
                    onClick={()=>navigate('/signup')}
                />
            </div>
        </div>

    );
};

export default Login;