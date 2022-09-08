import React, {useEffect, useState} from "react";
import {Container, Table} from "semantic-ui-react";
import {getAPIURL} from "../utils";
import MenuBar from "./menu_bar";

function niceBytes(x){
 const units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  let l = 0, n = parseInt(x, 10) || 0;
  while(n >= 1024 && ++l){
      n = n/1024;
  }
  return(n.toFixed(n < 10 && l > 0 ? 1 : 0) + ' ' + units[l]);
}

const ListRequests = () => {
  const init = new Date()
  const [date, setDate] = useState(init)

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
                setInProgress(data.in_progress);
            })
    }

    let rows = [];
    if(stlFiles !== null) {
        stlFiles.forEach((stl) => {
            rows.push(<Table.Row key={stl.name}>
                <Table.Cell><a href={"/view?filename="+stl.name}>{stl.name}</a></Table.Cell>
                <Table.Cell>{niceBytes(stl.filesize)}</Table.Cell>
                <Table.Cell>{stl.status}</Table.Cell>
                <Table.Cell><a href={stl.url}>Download</a></Table.Cell>
            </Table.Row>);
        })
    }

    if(inProgress !== null) {
        rows.push(<Table.Row key={"in progress"}>
            <Table.Cell>{inProgress.name}</Table.Cell>
            <Table.Cell></Table.Cell>
            <Table.Cell>building {Math.round(inProgress.progress*10000)/100}%</Table.Cell>
            <Table.Cell></Table.Cell>
        </Table.Row>)
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