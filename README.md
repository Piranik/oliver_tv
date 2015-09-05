# Oliver TV

[Demo](http://olivertv.duckdns.org)

## Running

If you don't want to host on the Pi use SSH FS, e.g.

```bash
sshfs name@mainserver:/location/of/oliver_tv/static mount
```

And then you can just run ```nohup pythone takePicture &``` on the Pi and on the server run ```nohup python server.py &```. Or, if you're using ```forever```,

```bash
forever start -c python server.py
```

