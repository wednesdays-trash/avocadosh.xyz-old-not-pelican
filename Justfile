alias gen := generate

all: generate generate-cv

generate:
    poetry run python generate.py

generate-cv:
    just -f pandoc-cv/Justfile all
    cp pandoc-cv/output/* static/

watch:
    python -m http.server --directory static &
    watchexec "poetry run python generate.py --no-collage"
