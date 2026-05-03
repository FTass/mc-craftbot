import './Header.css'
import steveImg from '../../assets/steve.svg'

function Header() {
  return (
    <header className="header">
      <div className="container">
        <div className="row align-items-center">
          <div className="col-12 col-md-2">
            <div className="header_logo">
              <img src={steveImg} alt="Logo de MC Craftbot" />
            </div>
          </div>

          <div className="col-12 col-md-10">
            <div className="header__brand">
              <h1>MC Craftbot</h1>
              <p>Tu asistente para craftear en Minecraft paso a paso</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header