import "./chat.css";
import MessageBubble from "./MessageBubble";

function Chat() {
  const messages = [
    { id: 1, role: "bot", text: "Hola" },
    { id: 2, role: "user", text: "Buenas" },
    { id: 3, role: "bot", text: "¿Cómo estás?" },
    { id: 4, role: "bot", text: "Te voy a decir algo" },
    { id: 5, role: "user", text: "Nooo" },
    { id: 6, role: "bot", text: "Lo siento, no te entiendo" },
    { id: 7, role: "user", text: "Mish" },
  ];

  return (
    <div className="container-fluid">
      <div className="row justify-content-center">
        <div className="col-md-8">
          <div className="chat_body d-flex flex-column">
            <div className="col-12 d-flex justify-content-center">
              <h2>¡Bienvenido a MC Craftbot!</h2>
            </div>

            {}
            <div className="col-12 flex-grow-1">
              <div className="messages_container">
                {messages.map((msg) => (
                  <MessageBubble key={msg.id} role={msg.role} text={msg.text} />
                ))}
              </div>
            </div>

          
            <div className="col-12">
              <div className="chat_input form-control">
                <input type="text" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
