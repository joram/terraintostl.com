import React, {useState} from "react";
import {Dropdown, Image, Menu} from "semantic-ui-react";
import {Link} from "react-router-dom";
import LoginButton, {Logout} from "./login_button";

function MenuBar() {
    let [activeItem, setActiveItem] = useState("home");

    let handleItemClick = (e, { name }) => {
        setActiveItem(name)
    }

    let loginButton = <LoginButton/>
    return <Menu inverted style={{margin:0}} attached="top">
        <Menu.Item
          name='home'
          active={activeItem === 'home'}
          onClick={handleItemClick}
          as={Link} to={"/"}
        >
            <Image src={"/mountain.png"} avatar />
            <span style={{paddingLeft:"5px"}}>Terrain To STL</span>
        </Menu.Item>

        <Menu.Item
          name='Downloads'
          active={activeItem === 'Downloads'}
          onClick={handleItemClick}
          as={Link} to={"/requests"}
        />

        {/*<Menu.Item position="right" name='' />*/}
        <Dropdown icon={loginButton} simple as={Menu.Item} position="right" style={{padding:"0px"}}>
            <Dropdown.Menu>
                <Dropdown.Item text='Saved STLs' as={Link} to={"/requests"} />
                <Dropdown.Item text='Logout' onClick={Logout}/>
            </Dropdown.Menu>
        </Dropdown>
    </Menu>
}


export default MenuBar;