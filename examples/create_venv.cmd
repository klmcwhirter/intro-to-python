
rd /q/s .venv

python -m venv .venv

call .\.venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r .\examples\requirements.txt

pip install -r .\examples\requirements.dev.txt
