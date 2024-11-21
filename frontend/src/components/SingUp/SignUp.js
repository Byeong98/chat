import React from 'react';
import styles from './SignUp.module.css'

const SignUp = () => {
    
    const handleSubmit =() =>{}

    return (
        <div className={styles.login_container}>
            <div className={styles.chat_title}>
                <h2>회원가입</h2>
            </div>
                <form className={styles.login_input_container} 
                        onSubmit={handleSubmit}>
                    <div className={styles.input_group}>
                        <label htmlFor="nickname">닉네임</label>
                        <input
                            type="text"
                            id="nickname"
                            name="nickname"
                            placeholder="닉네임 입력"
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
                        회원가입
                    </button>
                </form>
        </div>

    );
};

export default SignUp;