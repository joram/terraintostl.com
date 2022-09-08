import React, {useState} from "react";
import {Menu} from "semantic-ui-react";
import {Link} from "react-router-dom";

function MenuBar() {
    let [activeItem, setActiveItem] = useState("home");

    let handleItemClick = (e, { name }) => setActiveItem(name)
    return       <Menu inverted style={{margin:0}} >
        <Menu.Item
          name='home'
          active={activeItem === 'home'}
          onClick={handleItemClick}
          as={Link} to={"/"}
        />
        <Menu.Item
          name='Downloads'
          active={activeItem === 'Downloads'}
          onClick={handleItemClick}
          as={Link} to={"/requests"}
        />

        {/*<Menu.Menu position='right'>*/}
        {/*  <Menu.Item*/}
        {/*    name='logout'*/}
        {/*    active={activeItem === 'logout'}*/}
        {/*    onClick={handleItemClick}*/}
        {/*  />*/}
        {/*</Menu.Menu>*/}
      </Menu>

}


export default MenuBar;