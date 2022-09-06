import './App.css';

import React, {useState} from 'react';
import {DrawingManager, GoogleMap, LoadScript} from '@react-google-maps/api';
import {Button, Container, Dimmer, Form, Header, Icon, Loader, Menu, Segment, Table} from "semantic-ui-react";
import {BrowserRouter, Switch, Route, Link} from "react-router-dom";
import {useLocation} from "react-router-dom/cjs/react-router-dom";
import {Redirect} from "react-router-dom";

const containerStyle = {
  width: '100%',
  height: '100vh'
};

const center = {
  lat: 49.1026,
  lng: -123.4753
};

function MenuBar() {
    let [activeItem, setActiveItem] = useState("home");

    let handleItemClick = (e, { name }) => setActiveItem(name)
    return       <Menu inverted style={{margin:0}} >
        <Menu.Item
          name='home'
          active={activeItem === 'home'}
          onClick={handleItemClick}
        />


        <Menu.Menu position='right'>
          <Menu.Item
            name='logout'
            active={activeItem === 'logout'}
            onClick={handleItemClick}
          />
        </Menu.Menu>
      </Menu>

}

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

function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}

function RequestSTL() {
    let [resolution, setResolution] = useState(1);
    let [redirectURL, setRedirectURL] = useState(null);
    let [name, setName] = useState("vancouver island");
    let [zScale, setZScale] = useState(1);
    let query = useQuery();
    let region = query.get("region");

    function onSubmit(){
        console.log("submit", region, resolution, name, zScale);
        setRedirectURL("/request/submit?region=" + region + "&resolution=" + resolution + "&name=" + name + "&zScale=" + zScale);
    }
    if(redirectURL !== null){
        return <Redirect to={redirectURL} />
    }

      return (<>
            <MenuBar/>
              <Segment>
                <Header>Request STL</Header>
                  <Form>
                      <Form.Field inline>
                          <label>Name</label>
                          <input
                              defaultValue={name}
                              onChange={(event) => {setName(event.target.value)}}
                          />
                      </Form.Field>
                      <Form.Field inline>
                          <label>Polygon</label>
                          <input defaultValue={region} hidden={true}></input>
                      </Form.Field>
                      <Form.Field inline>
                          <label>Resolution</label>
                          <input
                              defaultValue={resolution}
                              type={"number"}
                              min={1}
                              max={10}
                              onChange={(event) => {setResolution(parseInt(event.target.value))}}
                          />
                      </Form.Field>
                      <Form.Field inline>
                          <label>Z-Scaling</label>
                          <input
                              defaultValue={zScale}
                              type={"number"}
                              min={1}
                              max={10}
                              onChange={(event) => {setZScale(parseInt(event.target.value))}}
                          />
                      </Form.Field>
                      <Button primary onClick={onSubmit}>Request</Button>
                  </Form>
              </Segment>
        </>
    )

}

function SubmitRequest() {
    let query = useQuery();
    let region = query.get("region");
    let resolution = query.get("resolution");
    let name = query.get("name");
    let zScale = query.get("zScale");
    let [requested, setRequested] = useState(false);
    let [response, setResponse] = useState(null);
    let [error, setError] = useState(null);
    if(!requested) {
        setRequested(true);
        let body = {
            name: name,
            region: region,
            resolution: resolution,
            z_scale: zScale
        }
        console.log(body)
        fetch("http://localhost:8000/stl", {
            // mode: 'no-cors',
            method: 'POST',
            headers: {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        }).then(response => response.json())
            .then(data => {
                if(data.detail!==undefined){
                    setError(JSON.stringify(data))
                } else {
                    setResponse(data);
                }
            })
            .catch((error) => {
                console.log(error)
                setError(error);
            });
    }

    if (response === null && error === null) {
        return <>
            <MenuBar/>
            <Segment basic>
                <Dimmer active inverted>
                  <Loader />
                </Dimmer>
            </Segment>
        </>
    }

    if (error !== null) {
        return <>
            <MenuBar/>
            <Segment basic>
                {error.toString()}
            </Segment>
        </>
    }

    return <Redirect to={"/requests"} />
}


function Requests() {

    let [stlFiles, setStlFiles] = useState([]);
    if(stlFiles.length === 0) {
        fetch("http://localhost:8000/stls", {
            // mode: 'no-cors',
            method: 'GET',
            headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json',
            },
        }).then(response => response.json())
            .then(data => {
                console.log(data)
                setStlFiles(data.stls);
            })
    }

    let rows = [];
    stlFiles.forEach((stl) => {
        rows.push(<Table.Row>
            <Table.Cell>{stl.name}</Table.Cell>
            <Table.Cell>{stl.triangles}</Table.Cell>
            <Table.Cell>{stl.filesize}</Table.Cell>
            <Table.Cell>{stl.status}</Table.Cell>
            <Table.Cell><a href={stl.url}>Download</a></Table.Cell>
        </Table.Row>);
    })
    return <>
        <MenuBar/>
        <Container>
        <Table celled>
    <Table.Header>
      <Table.Row>
        <Table.HeaderCell>Name</Table.HeaderCell>
        <Table.HeaderCell>Triangle Count</Table.HeaderCell>
        <Table.HeaderCell>Filesize</Table.HeaderCell>
        <Table.HeaderCell>Status</Table.HeaderCell>
        <Table.HeaderCell>Download</Table.HeaderCell>
      </Table.Row>
    </Table.Header>

    <Table.Body>
        {rows}
    </Table.Body>
  </Table>
        </Container>
    </>
}

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Switch>
                  <Route exact path='/' component={Map}></Route>
                  <Route exact path='/request' component={RequestSTL}></Route>
                  <Route exact path='/request/submit' component={SubmitRequest}></Route>
                  <Route exact path='/requests' component={Requests}></Route>
                </Switch>
            </BrowserRouter>
        </div>
    );
}

export default App;
