# SessionOpener
Ignition client session opener API using Flask & Selenium. This code uses the host machine's browser (Chrome) to run the various commands.

## API
The Flask server is run on the host machine at IP: localhost (0.0.0.0/127.0.0.1) & Port: 5000. All endpoints listed below use the POST http method.

### Endpoints
- #### startBrowser
  - **Start the chrome browser with a single session open that is directed to the deviceIP/devicePort specified in the request.**
  - Args:
    - deviceIP: IP address that the device gateway is on.
    - devicePort: Port that the device gateway is running on.
- #### endBrowser
  - Close the current browser but keep the Flask server running. 
  - Args: *None*
- #### addSession
  - **Add a new session to the open browser.**
  - Args: *None*
- #### removeSession
  - **Remove the last session added to the browser.**
  - Args: *None*
- #### shutdown
  - **Shutdown the Flask server.**
  - Args: *None*
- #### testing
  - **API testing endpoint that returns the current datetime.**
  - Args: *None*
  
### Sample Response
> .../startBrowser?deviceIP=localhost&devicePort=8088
```json
{
  "benchmarks": 
    {
      "currentCount": 1
      , "maxCount" : 1
    }
  , "status": 
    {
      "message" : "No Error"
      , "value": true
    }
}
```
