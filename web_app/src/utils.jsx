import {useLocation} from "react-router-dom";
import React from "react";

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

export {getAPIURL, useQuery}
