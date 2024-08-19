# Setting up the stack

## Install cli
```bash
curl -s https://api.github.com/repos/vmfarms/sidepro/releases/latest \
    | grep "browser_download_url.*sidepro" \
    | cut -d : -f 2,3 \
    | tr -d \" \
    | wget -qi - -O sidepro && \
    chmod +x sidepro && \
    sudo mv sidepro /usr/local/bin
```

## login

## Deploy
```bash
sidepro push --name terraintostl.com --path ./server
```