import React, {useState} from "react";
import {Image, Menu} from "semantic-ui-react";
import {Link} from "react-router-dom";
import LoginModal from "./login_modal";

function MenuBar() {
    let [activeItem, setActiveItem] = useState("home");

    let handleItemClick = (e, { name }) => {
        setActiveItem(name)
    }

    return <>
        <Menu inverted style={{margin:0}} >
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

        <Menu.Menu position='right'>
          <LoginModal/>
        </Menu.Menu>
      </Menu>
    </>

}


export default MenuBar;