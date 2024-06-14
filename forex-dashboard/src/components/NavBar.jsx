import React from 'react'

import NavBarLink from './NavBarLink'


function NavBar() {
  return (
    <div id="navbar">

      <div className="navtitle">4X</div>

      <div id="navlinks">
        <NavBarLink path="/" text="Home" />
        <NavBarLink path="/dashboard" text="Dashboard" />
      </div>

    </div>
  )
}

export default NavBar
