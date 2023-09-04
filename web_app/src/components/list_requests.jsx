import React, {useEffect, useState} from "react";
import {Container, Table} from "semantic-ui-react";
import {getAPIURL, niceBytes} from "../utils";
import MenuBar from "./menu_bar";
import Cookies from "universal-cookie";

const cookies = new Cookies();


const ListRequests = () => {
  const init = new Date()
  const [, setDate] = useState(init)

    const tick = () => {
        setDate(new Date())
    }

    useEffect(() => {
        const timerID = setInterval(() => tick(), 100)
        return () => {
            clearInterval(timerID)
        }
    })


    let [stlFiles, setStlFiles] = useState(null);
    let [inProgress, setInProgress] = useState(null);
    if(stlFiles === null) {
        let sessionDetails = cookies.get('sessionDetails', { path: '/' })
        console.log("sessionDetails:", sessionDetails)

        let session_key = null
        if(sessionDetails !== undefined){
            session_key = sessionDetails.session_key
        }
        fetch(getAPIURL()+"/stls", {
            // mode: 'no-cors',
            method: 'GET',
            headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json',
                "session_key": session_key,
            },
        }).then(response => response.json())
            .then(data => {
                console.log(data)
                setStlFiles(data.stls);
                setInProgress(data.in_progress);
            })
    }

    let rows = [];
    if(stlFiles !== null) {
        stlFiles.forEach((stl) => {
            rows.push(<Table.Row key={stl.name}>
                {/*<Table.Cell><a href={"/view?filename="+stl.name}>{stl.name}</a></Table.Cell>*/}
                <Table.Cell>{stl.name}</Table.Cell>
                <Table.Cell>{niceBytes(stl.filesize)}</Table.Cell>
                <Table.Cell>{stl.status}</Table.Cell>
                <Table.Cell><a href={stl.url}>Download</a></Table.Cell>
            </Table.Row>);
        })
    }

    if(inProgress !== null) {
        inProgress.forEach((request) => {
            rows.push(<Table.Row key={"in progress"}>
                <Table.Cell>{request.name}</Table.Cell>
                <Table.Cell></Table.Cell>
                <Table.Cell>building {Math.round(request.progress * 10000) / 100}%</Table.Cell>
                <Table.Cell></Table.Cell>
            </Table.Row>)
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