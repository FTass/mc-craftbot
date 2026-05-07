import { useEffect, useMemo, useRef, useState } from 'react'
import './chat.css'
import steveIcon from '../../assets/steve.svg'
import botIcon from '../../assets/bot.svg'

const CHAT_API_URL = import.meta.env.VITE_CHAT_API_URL || 'http://127.0.0.1:8000/chat'

const INITIAL_SUGGESTIONS = [
  '¿Cómo hago una mesa de crafteo?',
  '¿Cómo hago un pico de madera?',
  '¿Cómo hago una espada de hierro?',
]

function getMessageTime() {
  return new Intl.DateTimeFormat('es-CL', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(new Date())
}

function createUserMessage(text) {
  return {
    id: crypto.randomUUID(),
    role: 'user',
    text,
    time: getMessageTime(),
  }
}

function createBotMessage(data, fallbackSource) {
  const answer = data?.answer || 'No recibí una respuesta válida desde el backend.'

  return {
    id: crypto.randomUUID(),
    role: 'bot',
    text: answer,
    time: getMessageTime(),
    status: data?.status || 'ok',
    matchedItem: data?.matched_item || null,
    matchedRecipeId: data?.matched_recipe_id || null,
    source: data?.source || fallbackSource || null,
  }
}

function MessageText({ text }) {
  const lines = String(text || '').split('\n').filter(Boolean)
  const bulletLike = lines.length > 1 && lines.some((line) => /^[-•*\d.)\s]/.test(line.trim()))

  if (bulletLike) {
    return (
      <div className="chat_message__boxed_text">
        {lines.map((line) => (
          <p key={line}>▪ {line.replace(/^[-•*\d.)\s]+/, '').trim()}</p>
        ))}
      </div>
    )
  }

  return (
    <p className="chat_message__text">
      {lines.length > 0 ? lines.join('\n') : text}
    </p>
  )
}

function ChatMessage({ message }) {
  const isUser = message.role === 'user'

  return (
    <article className={`chat_message chat_message--${isUser ? 'user' : 'bot'}`}>
      <img
        className="chat_message__avatar"
        src={isUser ? steveIcon : botIcon}
        alt={isUser ? 'Avatar del usuario' : 'Avatar de MC Craftbot'}
      />

      <div className="chat_message__body">
        <div className="chat_message__meta">
          <strong>{isUser ? 'TÚ' : 'MC CRAFTBOT'}</strong>
          <span>{message.time}</span>
        </div>

        <MessageText text={message.text} />
      </div>
    </article>
  )
}

function Chat() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const messagesEndRef = useRef(null)

  const visibleMessages = useMemo(() => messages, [messages])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [visibleMessages, isLoading])

  const sendMessage = async (rawMessage) => {
    const trimmedMessage = rawMessage.trim()

    if (!trimmedMessage || isLoading) {
      return
    }

    const userMessage = createUserMessage(trimmedMessage)
    setMessages((previousMessages) => [...previousMessages, userMessage])
    setInputValue('')
    setError('')
    setIsLoading(true)

    try {
      const response = await fetch(CHAT_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: trimmedMessage }),
      })

      if (!response.ok) {
        throw new Error(`El backend respondió con estado ${response.status}.`)
      }

      const data = await response.json()
      const botMessage = createBotMessage(data, 'backend')
      setMessages((previousMessages) => [...previousMessages, botMessage])
    } catch (requestError) {
      const errorMessage =
        requestError instanceof Error
          ? requestError.message
          : 'No se pudo consultar el backend.'

      setError(`${errorMessage} Verifica que FastAPI esté activo en http://127.0.0.1:8000.`)

      const botErrorMessage = createBotMessage(
        {
          status: 'error',
          answer:
            'No pude conectar con el backend del chatbot. Verifica que FastAPI esté ejecutándose y que Ollama esté disponible.',
        },
        'frontend',
      )

      setMessages((previousMessages) => [...previousMessages, botErrorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    sendMessage(inputValue)
  }

  const handleClearChat = () => {
    setMessages([])
    setError('')
    setInputValue('')
  }

  return (
    <section className="chat_frame" aria-label="Chat de recetas de Minecraft">
      <div className="chat_log" aria-live="polite">
        {visibleMessages.length === 0 && !isLoading && (
          <div className="chat_empty_state">
            <div className="chat_empty_state__icon">▦</div>
            <div>
              <h2>Pregúntame por un crafteo</h2>
              <p>Ejemplos rápidos:</p>
              <div className="chat_empty_state__buttons">
                {INITIAL_SUGGESTIONS.map((suggestion) => (
                  <button
                    type="button"
                    key={suggestion}
                    onClick={() => sendMessage(suggestion)}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {visibleMessages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {isLoading && (
          <article className="chat_message chat_message--bot chat_message--loading">
            <img className="chat_message__avatar" src={botIcon} alt="Avatar de MC Craftbot" />
            <div className="chat_message__body">
              <div className="chat_message__meta">
                <strong>MC CRAFTBOT</strong>
                <span>{getMessageTime()}</span>
              </div>
              <p className="chat_message__text">Consultando recetas...</p>
            </div>
          </article>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="chat_input_bar" onSubmit={handleSubmit}>
        <label className="sr_only" htmlFor="chat-input">
          Escribe tu pregunta sobre crafteos
        </label>
        <div className="chat_input_bar__field">
          <span aria-hidden="true">⌕</span>
          <input
            id="chat-input"
            type="text"
            value={inputValue}
            onChange={(event) => setInputValue(event.target.value)}
            placeholder="Escribe tu pregunta sobre crafteos..."
            disabled={isLoading}
            autoComplete="off"
          />
        </div>
        <button
          className="chat_input_bar__send"
          type="submit"
          disabled={isLoading || !inputValue.trim()}
        >
          Enviar
        </button>
      </form>

      {error && <div className="chat_error" role="alert">{error}</div>}

      <footer className="chat_status_bar">
        <div className="chat_status_bar__status">
          <span aria-hidden="true" />
          Conectado
        </div>
        <div className="chat_status_bar__version">
          <span aria-hidden="true">▣</span>
          MC Craftbot v1.0.0
        </div>
        <button type="button" onClick={handleClearChat}>
          Limpiar chat
        </button>
      </footer>
    </section>
  )
}

export default Chat
