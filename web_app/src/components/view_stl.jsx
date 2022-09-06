import {StlViewer} from "react-stl-viewer";
import React from "react";
import MenuBar from "./menu_bar";
import {getAPIURL, useQuery} from "../utils";

function ViewSTL() {
    let query = useQuery();
    let filename = query.get("filename");
    const url = getAPIURL()+"/static/"+filename
    console.log(url)
    const style = {
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
    }

    return (
        <>
            <MenuBar/>
            <StlViewer
                style={style}
                orbitControls
                shadows
                showAxes
                modelProps={{
                    color: "#008675",
                    scale: 20
                }}
                url={url}
            />
        </>
    );
}

export default ViewSTL;