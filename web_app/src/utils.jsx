import {useLocation} from "react-router-dom";
import React from "react";
import Cookies from 'universal-cookie'

const cookies = new Cookies();

function getAPIURL() {
    let baseURL = "https://terraintostlapi.oram.ca"
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
        baseURL = "http://localhost:8000"
    }
    return baseURL;
}

function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}

function niceBytes(x){
 const units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  let l = 0, n = parseInt(x, 10) || 0;
  while(n >= 1024 && ++l){
      n = n/1024;
  }
  return(n.toFixed(n < 10 && l > 0 ? 1 : 0) + ' ' + units[l]);
}

function isLoggedIn() {
    return cookies.get('googleCreds') !== undefined;
}

export {getAPIURL, useQuery, niceBytes, isLoggedIn}
