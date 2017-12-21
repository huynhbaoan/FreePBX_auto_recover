# FreePBX auto recover
Auto monitor and recover FreePBX service if crash.

1. Scenerio:

This script can be used to monitor any FreePBX instance. It is extremely handly when come to monitor FreePBX with WebRTC enabled.
FreePBX use Apache server to handle websocket connections. Unfortunately, some NodeJS libraries for WebRTC don't handle websocket connection properly, lead to websocket connection leaking. In these case, your server will stop accepting new connection, and drop any calls.
The proper solution in this case is fixing the library, of course. But what if you're unable to do it?
Well, just use this script and let your FreePBX take care of itself.

This script will check the number of active calls, active channels, leaked websocket connection. Base on our definition, it can do a soft restart to release leaked websocket or an mergency restart in case your service is totally dead.

2. Setup:

Place 3 bash files in a same directory, setup a root crontab for asterisk_health_monitor.sh, adjust number of connections to match your needs, and go to sleep.
