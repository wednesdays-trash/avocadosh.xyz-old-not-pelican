alias gen := generate

generate:
    poetry run python generate.py

watch:
    just serve &
    watchexec "poetry run python generate.py --no-collage"

serve:
    python -m http.server --directory static
