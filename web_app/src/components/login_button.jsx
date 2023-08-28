import React from 'react'
import {Image, Menu} from 'semantic-ui-react'
import Cookies from 'universal-cookie'
import LoginModal from "./login_modal";

const cookies = new Cookies();

function Logout() {
    cookies.remove('googleCreds')
    cookies.remove('sessionDetails')
    window.location.reload()
}

function LoginButton() {
  if(cookies.get('googleCreds') !== undefined) {
    return <>
        <Menu.Item>
            <span style={{paddingRight:"5px"}}>{cookies.get('sessionDetails').email}</span>
            <Image src={cookies.get('sessionDetails').picture} size="mini" avatar/>
        </Menu.Item>
    </>
  }

  let trigger = <Menu.Item>Login</Menu.Item>
  return <LoginModal trigger={trigger}/>
}

export default LoginButton
export {Logout}