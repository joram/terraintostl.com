import React, {useState} from "react";
import {Button, Header, Icon, Segment} from "semantic-ui-react";
import {Link} from "react-router-dom";
import {DrawingManager, GoogleMap, LoadScript} from "@react-google-maps/api";
import MenuBar from "./menu_bar";
import {isLoggedIn as isLoggedInFunc} from "../utils";
import LoginButton from "./login_button";

const containerStyle = {
  width: '100%',
  height: '100vh'
};

const center = {
  lat: 49.1026,
  lng: -123.4753
};

function Map() {
    let [popup, setPopup] = useState(null);
    let [, setIsLoggedIn] = useState(isLoggedInFunc());

    function loggedInPopup(region) {
        return <Segment placeholder style={{margin:0}} >
            <Header icon>
              <Icon name='pdf file outline' />
              You've selected an area. Would you like an STL file?
            </Header>
            <Button primary as={Link} to={`/request?region=${btoa(JSON.stringify(region))}`}>Request STL</Button>
          </Segment>
    }

    function loginRequiredPopup(region) {
        return <Segment placeholder style={{margin:0}} >
            <Header icon>
              <Icon name='pdf file outline' />
              You've selected an area. If you would like to request an STL file, please login.
            </Header>
            <LoginButton onLogin={() => {
                setIsLoggedIn(true)
                setPopup(loggedInPopup(region))
            }}/>
          </Segment>
    }

    const onPolygonComplete = poly => {
        let region = []
        poly.getPath().getArray().forEach((point) => {
            region.push([point.lat(), point.lng()])
        })

        if(isLoggedInFunc()){
            setPopup(loggedInPopup(region))
        } else {
            setPopup(loginRequiredPopup(region))
        }
    }


    return (<>
            <MenuBar/>
            {popup}
        <LoadScript googleMapsApiKey="AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g" libraries={['drawing']} >
            <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={8} >
                <DrawingManager onPolygonComplete={onPolygonComplete} />
            </GoogleMap>
        </LoadScript>
        </>
    )
}

export default Map;
