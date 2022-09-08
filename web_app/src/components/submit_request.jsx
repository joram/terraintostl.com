import React, {useState} from "react";
import {Dimmer, Loader, Segment} from "semantic-ui-react";
import {Navigate} from "react-router-dom";
import {getAPIURL, useQuery} from "../utils";
import MenuBar from "./menu_bar";


function SubmitRequest() {
    let query = useQuery();
    let region = query.get("region");
    let resolution = query.get("resolution");
    let name = query.get("name");
    let zScale = query.get("zScale");
    let bounds = query.get("bounds");
    let [requested, setRequested] = useState(false);
    let [response, setResponse] = useState(null);
    let [error, setError] = useState(null);
    if(!requested) {
        setRequested(true);
        let body = {
            name: name,
            region: region,
            resolution: resolution,
            z_scale: zScale,
            bounds: bounds,
        }
        console.log(body)
        fetch(getAPIURL()+"/stl", {
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

    return <Navigate to={"/requests"} />
}


export default SubmitRequest;