## Running

You can run script with docker or python

### Python
```shell
python main.py --config_file src/static_marker/config_sample.toml
```

### Cmd
```shell
poetry install
poetry run static_marker
```

### Docker
```shell
docker build -t StaticMarker .
docker run -it StaticMarker /bin/sh
python main.py
```
