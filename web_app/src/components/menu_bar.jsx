import React, {useState} from "react";
import {Image, Menu} from "semantic-ui-react";
import {Link} from "react-router-dom";
import {LoginMenuItem} from "./login_button";

function MenuBar() {
    let [activeItem, setActiveItem] = useState("home");

    let handleItemClick = (e, { name }) => {
        setActiveItem(name)
    }

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
        <LoginMenuItem/>
    </Menu>
}


export default MenuBar;