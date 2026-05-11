import Header from './components/header/Header'
import Chat from './components/chat/chat'
import './App.css'

function App() {
  return (
    <div className="app_shell">
      <div className="mc_window">
        <Header />
        <main className="app_main">
          <Chat />
        </main>
      </div>
    </div>
  )
}

export default App
