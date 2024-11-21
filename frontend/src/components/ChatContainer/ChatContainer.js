import React from 'react';
import styles from './ChatContainer.module.css'

const ChatContainer = () => {

    const handleMessageSubmit = () => { }
    return (
        <div className={styles.chat_container}>
            <div className={styles.chat_content_container}>

            </div>
            <div className={styles.chat_input_container}>
                <label
                    htmlFor="chat-image-input"
                    className={styles.chat_image_label}
                    >사진 선택</label>
                <input
                    className={styles.chat_image_input}
                    id="chat-image-input"
                    accept="image/*"
                    type="file"
                />

                <input
                    className={styles.chat_message_input}
                    id="chat-message-input"
                    type="text"
                    maxlength="50"
                    placeholder="메시지를 입력하세요"
                    aria-label="메시지 입력"
                />

                <input
                    className={styles.chat_message_submit}
                    id="chat-message-submit"
                    type="button"
                    value="Send"
                    onClick={handleMessageSubmit}
                />
            </div>
        </div>
    );
};

export default ChatContainer;