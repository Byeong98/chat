import React,{useState} from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './SignUp.module.css'
import axios from 'axios';

const SignUp = () => {
    const navigate = useNavigate();
    const [data, setData] = useState({
        'username': '',
        'email': '',
        'password': ''
    })

    const handleSignup = async () => {
        if (!data.username.trim()){
            alert('닉네임을 입력하세요')
        } else if(!data.email.trim() ){
            alert('이메일를 입력하세요')
        } else if(!data.password.trim()){
            alert('비밀번호를 입력하세요')
        } else {
            try {
                const response = await axios.post(
                    'http://localhost:8000/api/accounts/signup/',
                    {
                        username: data.username,
                        email: data.email,
                        password: data.password
                    }
                );
                alert(response.data.message)
                navigate('/login')
            } catch (error) {
                alert(error.response.data.message)
            }
        }
    }

    //input 입력갑 저장
    const handleCange = (name, value) => {
        setData({ ...data, [name]: value })
    }

    return (
        <div className={styles.login_container}>
            <div className={styles.chat_title}>
                <h2>회원가입</h2>
            </div>
                <div className={styles.login_input_container} >
                    <div className={styles.input_group}>
                        <label htmlFor="nickname">닉네임</label>
                        <input
                            type="text"
                            id="nickname"
                            name="nickname"
                            placeholder="닉네임 입력"
                            value={data.username}
                            onChange={e=>handleCange('username',e.target.value)}
                            required
                        />
                    </div>
                    <div className={styles.input_group}>
                        <label htmlFor="email">이메일</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            placeholder="이메일 입력"
                            value={data.email}
                            onChange={e=>handleCange('email',e.target.value)}
                            required
                        />
                    </div>
                    <div className={styles.input_group}>
                        <label htmlFor="password">비밀번호</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            placeholder="비밀번호 입력"
                            value={data.password}
                            onChange={e=>handleCange('password',e.target.value)}
                            required
                        />
                    </div>
                    <input type="button" 
                            className={styles.login_button}
                            onClick={handleSignup} 
                            value='회원가입'/>
                    
                </div>
        </div>

    );
};

export default SignUp;