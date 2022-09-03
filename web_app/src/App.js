import './App.css';

import React, {Component, useState} from 'react';
import { DrawingManager, GoogleMap, LoadScript } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '100vh'
};

const center = {
  lat: 49.1026,
  lng: -123.4753
};




function Map(props) {
    let {polygon, setPolygon} = useState([]);

    const onPolygonComplete = polygon => {
        console.log(polygon.getPath().getArray());
    }

    return (
        <LoadScript googleMapsApiKey="AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g" libraries={['drawing']} >
            <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={8} >
                <DrawingManager onPolygonComplete={onPolygonComplete} />
            </GoogleMap>
        </LoadScript>
    )
}


function App() {
    return (
        <div className="App">
            <Map/>
        </div>
    );
}

export default App;
