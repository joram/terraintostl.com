import './App.css';

import React from 'react';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import ViewSTL from "./components/view_stl";
import ListRequests from "./components/list_requests";
import SubmitRequest from "./components/submit_request";
import RequestSTL from "./components/request_stl";
import Map from "./components/map";

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Routes>
                  <Route exact path='/' element={<Map/>}></Route>
                  <Route exact path='/request' element={<RequestSTL/>}></Route>
                  <Route exact path='/request/submit' element={<SubmitRequest/>}></Route>
                  <Route exact path='/requests' element={<ListRequests/>}></Route>
                  <Route exact path='/view' element={<ViewSTL/>}></Route>
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
