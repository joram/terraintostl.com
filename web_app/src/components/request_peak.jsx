import React, {useState} from "react";
import {Navigate} from "react-router-dom";
import {Button, Form, Header, Segment} from "semantic-ui-react";
import MenuBar from "./menu_bar";
import {useQuery} from "../utils";

function RequestPeak() {
    let [resolution, setResolution] = useState(1.0);
    let [NavigateURL, setNavigateURL] = useState(null);
    let [name, setName] = useState("golden hinde");

    function onSubmit(){
        console.log("submit", resolution, name);
        setNavigateURL("/request/submit?name=" + name + "&resolution=" + resolution+"&request_type=peak");
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
                          <label>Peak Name</label>
                          <input
                              defaultValue={name}
                              onChange={(event) => {setName(event.target.value)}}
                          />
                      </Form.Field>
                      <Button primary onClick={onSubmit}>Request</Button>
                  </Form>
              </Segment>
        </>
    )

}

export default RequestPeak;
