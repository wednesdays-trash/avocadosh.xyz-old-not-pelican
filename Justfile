alias gen := generate

all: generate generate-cv

generate:
    poetry run python generate.py

generate-cv:
    just -f pandoc-cv/Justfile all
    cp pandoc-cv/output/* static/

watch:
    #!/bin/bash
    python -m http.server --directory static &
    # kill the static assets server when the watchexec process receives Ctrl-C
    trap "kill $!" SIGINT
    watchexec "poetry run python generate.py --no-collage"
