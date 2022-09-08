import React, {useState} from "react";
import {Navigate} from "react-router-dom";
import {Button, Form, Header, Segment} from "semantic-ui-react";
import MenuBar from "./menu_bar";
import {useQuery} from "../utils";

function RequestSTL() {
    let [resolution, setResolution] = useState(1);
    let [NavigateURL, setNavigateURL] = useState(null);
    let [name, setName] = useState("vancouver island");
    let [zScale, setZScale] = useState(1);
    let [bounds, setBounds] = useState("polygon");
    let query = useQuery();
    let region = query.get("region");

    function onSubmit(){
        console.log("submit", region, resolution, name, zScale);
        setNavigateURL("/request/submit?region=" + region + "&resolution=" + resolution + "&name=" + name + "&zScale=" + zScale+"&bounds="+bounds);
    }
    if(NavigateURL !== null){
        return <Navigate to={NavigateURL} />
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

                      <Form.Field inline>
                          <label>Bounds</label>
                          <Button.Group>
                              <Button name={"polygon"} onClick={()=> setBounds("polygon")} active={bounds==="polygon"}>fit to polygon</Button>
                              <Button name={"boundingbox"} onClick={()=> setBounds("boundingbox")} active={bounds==="boundingbox"}>fit to bounding box</Button>
                          </Button.Group>
                      </Form.Field>
                      <Button primary onClick={onSubmit}>Request</Button>
                  </Form>
              </Segment>
        </>
    )

}

export default RequestSTL;
