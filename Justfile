alias gen := generate

generate:
    poetry run python generate.py

watch:
    just serve &
    watchexec just generate

serve:
    python -m http.server --directory static
