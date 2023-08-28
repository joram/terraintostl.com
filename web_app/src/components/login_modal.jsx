import React from 'react'
import {Image, Menu, Modal} from 'semantic-ui-react'
import {GoogleLogin} from "@react-oauth/google"
import Cookies from 'universal-cookie'
import {getAPIURL} from "../utils";

const cookies = new Cookies();

function LoginModal(props) {
    let {trigger} = props
  const [open, setOpen] = React.useState(false)
  const [, setGoogleCreds] = React.useState(undefined)

    function callHomeWithCredentials(credentialResponse) {
        fetch(getAPIURL()+"/login", {
            method: 'POST',
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Accept": "application/json",
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(credentialResponse)
        }).then(response => response.json())
        .then(data => {
            cookies.set('googleCreds', credentialResponse, { path: '/' });
            cookies.set('sessionDetails', data, { path: '/' });
            setGoogleCreds(credentialResponse)
        })
    }

  if(cookies.get('googleCreds') !== undefined) {
    return <>
        <Menu.Item>
            <span style={{paddingRight:"5px"}}>{cookies.get('sessionDetails').email}</span>
            <Image src={cookies.get('sessionDetails').picture} size="mini" avatar/>
        </Menu.Item>
    </>
  }
  return (
    <Modal
      onClose={() => setOpen(false)}
      onOpen={() => setOpen(true)}
      open={open}
      trigger={trigger}
    >
      <Modal.Header>Login</Modal.Header>
      <Modal.Content>
        <Modal.Description>
          <p>
            To generate any STL files, you must first login with your Google account.
          </p>
        </Modal.Description>
      </Modal.Content>
      <Modal.Actions>
        <span>
          <GoogleLogin
            onSuccess={credentialResponse => {
              callHomeWithCredentials(credentialResponse);
              setOpen(false)
            }}
            onError={() => {
              console.log('Login Failed');
            }}
          />
        </span>
      </Modal.Actions>
    </Modal>
  )
}

export default LoginModal
