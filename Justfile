alias gen := generate

generate:
    poetry run python generate.py

serve:
    python -m http.server --directory static
