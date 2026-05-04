function MessageBubble({ role, text }) {
    return (
        <div className={`message ${role}`}>
            {text}
        </div>
    )
}

export default MessageBubble