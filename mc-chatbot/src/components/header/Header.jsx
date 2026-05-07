import './Header.css'
import botIcon from '../../assets/bot.svg'

function Header() {
  return (
    <header className="mc_header" aria-label="Encabezado de MC Craftbot">
      <button className="mc_header__square_button" type="button" aria-label="Menú de MC Craftbot">
        <img src={botIcon} alt="" aria-hidden="true" />
      </button>

      <div className="mc_header__title_box">
        <h1 className="mc_header__title">MC CRAFTBOT</h1>
        <p className="mc_header__subtitle">TU ASISTENTE DE CRAFTEOS</p>
      </div>

      <button className="mc_header__square_button mc_header__settings" type="button" aria-label="Configuración">
        ⚙
      </button>
    </header>
  )
}

export default Header
