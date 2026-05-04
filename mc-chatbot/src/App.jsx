import { useState } from 'react'
import Header from './components/header/Header'
import Chat from './components/chat/chat'
import './App.css'

function App() {
  return (
    <>
      <Header />
      <main>
        <Chat />
      </main>
    </>
  )
}

export default App