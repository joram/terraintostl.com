import React, {useState} from "react";
import {Container, Table} from "semantic-ui-react";
import {getAPIURL} from "../utils";
import MenuBar from "./menu_bar";


function ListRequests() {

    let [stlFiles, setStlFiles] = useState(null);
    if(stlFiles === null) {
        fetch(getAPIURL()+"/stls", {
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
    if(stlFiles !== null) {
        stlFiles.forEach((stl) => {
            rows.push(<Table.Row>
                <Table.Cell><a href={"/view?filename="+stl.name}>{stl.name}</a></Table.Cell>
                <Table.Cell>{stl.filesize}</Table.Cell>
                <Table.Cell>{stl.status}</Table.Cell>
                <Table.Cell><a href={stl.url}>Download</a></Table.Cell>
            </Table.Row>);
        })
    }

    return <>
        <MenuBar/>
        <Container>
        <Table celled>
    <Table.Header>
      <Table.Row>
        <Table.HeaderCell>Name</Table.HeaderCell>
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

export default ListRequests;