import React, {useState} from "react";
import {Button, Header, Icon, Segment} from "semantic-ui-react";
import {Link} from "react-router-dom";
import {DrawingManager, GoogleMap, LoadScript} from "@react-google-maps/api";
import MenuBar from "./menu_bar";

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

    const onPolygonComplete = poly => {
        let region = []
        poly.getPath().getArray().forEach((point) => {
            region.push([point.lat(), point.lng()])
        })

        setPopup(<Segment placeholder style={{margin:0}} >
        <Header icon>
          <Icon name='pdf file outline' />
          You've selected an area. Would you like an STL file?
        </Header>
        <Button primary as={Link} to={`/request?region=${btoa(JSON.stringify(region))}`}>Request STL</Button>
      </Segment>)
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
