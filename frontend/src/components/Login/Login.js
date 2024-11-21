import React from 'react';
import styles from './Login.module.css'

const Login = () => {

    const handleSubmit =() =>{

    }

    return (
        <div className={styles.login_container}>
            <div className={styles.chat_title}>
                <h2>로그인</h2>
            </div>
                <form className={styles.login_input_container} 
                        onSubmit={handleSubmit}>
                    <div className={styles.input_group}>
                        <label htmlFor="email">이메일</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            placeholder="이메일 입력"
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
                            required
                        />
                    </div>
                    <button type="submit" className={styles.login_button}>
                        로그인
                    </button>
                </form>
            <div className={styles.signup_container}>
                <hr/>
                <input 
                    className={styles.login_button}
                    type='button' 
                    value='회원가입' 
                />
            </div>
        </div>

    );
};

export default Login;