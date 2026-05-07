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
    { id: 9, role: "bot", text: "para craftear un pico de madera, necesitas dos palos y 3 bloques de cualquier madera, en al configuracion: {[madera, madera, madera]. [0, palo, 0]. [0, palo, 0]}" },
  ];

  return (
    <div className="container-fluid">
      <div className="row justify-content-center">
        <div className="col-md-8 p-5 my-1">
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
              <form className="chat_input">
                <div className="input_wrapper my-3">
                  <input type="text" className="form-control chat-form" />
                  <button type="submit" className="btn send_btn">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="22"
                      height="22"
                      fill="currentColor"
                      viewBox="0 0 16 16"
                      aria-hidden="true"
                    >
                      <path d="M15.854.146a.5.5 0 0 0-.527-.11l-15 6a.5.5 0 0 0 .006.932L5.5 9.25V14.5a.5.5 0 0 0 .832.374l2.57-2.304 3.5 2.25a.5.5 0 0 0 .768-.32l2.5-13a.5.5 0 0 0-.316-.604zM6 8.933l7.724-6.186L6 9.75v-0.817z" />
                    </svg>
                  </button>
                </div>
              </form>  
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
