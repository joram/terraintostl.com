import React from 'react'
import {Button, Dropdown, Image, Menu} from 'semantic-ui-react'
import Cookies from 'universal-cookie'
import LoginModal from "./login_modal";
import {Link} from "react-router-dom";

const cookies = new Cookies();

function Logout() {
    cookies.remove('googleCreds')
    cookies.remove('sessionDetails')
    window.location.reload()
}

function LoginButton(props) {
    let {onLogin} = props
    let button = <Button>Login</Button>
    return <LoginModal trigger={button} onLogin={onLogin}/>
}
function LoginMenuItem() {
    let [isLoggedIn, setIsLoggedIn] = React.useState(cookies.get('googleCreds') !== undefined);

  if(isLoggedIn) {
    let button = <Menu.Item>
        <span style={{paddingRight:"5px"}}>
            {cookies.get('sessionDetails').email}
        </span>
        <Image src={cookies.get('sessionDetails').picture} size="mini" avatar/>
    </Menu.Item>

    return <Dropdown icon={button} simple as={Menu.Item} position="right" style={{padding:"0px"}}>
        <Dropdown.Menu>
            <Dropdown.Item text='Saved STLs' as={Link} to={"/requests"} />
            <Dropdown.Item text='Logout' onClick={Logout}/>
        </Dropdown.Menu>
    </Dropdown>
  }

  let trigger = <Menu.Item position="right">Login</Menu.Item>
  return <LoginModal trigger={trigger} onLogin={() => {
        setIsLoggedIn(true)
  }}/>
}

export default LoginButton
export {Logout, LoginMenuItem}