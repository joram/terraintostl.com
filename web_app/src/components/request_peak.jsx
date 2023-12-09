import React, {useState} from "react";
import {Navigate} from "react-router-dom";
import {Button, Form, Header, Segment} from "semantic-ui-react";
import MenuBar from "./menu_bar";
import {getAPIURL, useQuery} from "../utils";

function RequestPeak() {
    let [resolution, setResolution] = useState(1.0);
    let [NavigateURL, setNavigateURL] = useState(null);
    let [name, setName] = useState("everest");
    let [searchResults, setSearchResults] = useState(null);
        let query = useQuery();

    function search(){
        console.log("search", name);
        let query_url = getAPIURL()+"/search?query=" + name;
        fetch(query_url, {
            method: 'GET',
            headers: {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            },
        }).then(response => response.json())
            .then(data => {
                setSearchResults(data["results"]);
                console.log(data);
            })
    }

    if(NavigateURL !== null){
        return <Navigate to={NavigateURL} />
    }

    let resultsSegment = null;
    if(searchResults && searchResults.length > 0){
         resultsSegment = <Segment>
            <Header>Search Results</Header>
            <ul>
                {searchResults.map((result) => {
                    return <li key={result.id}><a href={"/request/submit?request_type=peak&name="+result.name+"&resolution=1"}>
                        {result.content.properties.countries[0]}, {result.name}
                    </a></li>
                }
                )}
            </ul>
        </Segment>
    }
    if(searchResults && searchResults.length === 0){
         resultsSegment = <Segment>
            <Header>Search Results</Header>
            <ul>
                <li>Nothing Found</li>
            </ul>
        </Segment>
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
                      <Button primary onClick={search}>Request</Button>
                  </Form>
              </Segment>
              {resultsSegment}
        </>
    )

}

export default RequestPeak;
