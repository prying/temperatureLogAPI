# Temperature Log API
this project uses Flask to create and api to lot the temperature.

## Run
to run this flask app set `FLASK_APP` to app i.e `set FLASK_APP=app`, then to run `flask run`

### usage
to use most, if not all the of the functionality of the API you first need to gen a `key` with `/getkey`, with the 
key it returns you can now put it after and API function to use that keys data i.e:
`/update?key=YOURKEY&temp=0` updates `YOURKEY`'s temp data with a value of 0.

API calls are: <br />
`/getkey` to create a new key. <br />
`/` gives users a plot of the temps. <br />
`/update` with parameters of `temp`. <br />
`/remove/log` to remove that keys log. <br />
`/remove/key` to remove that key. <br />

place confidential configs in `/instance/config.py` and be sure its on the .gitignore or check its not in staging 


