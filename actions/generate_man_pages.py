name: Generate and Publish Man Page

on:
  push:
    branches: [main]

permissions: read
  contents: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install groff and python-qrcode
        run: |
          sudo apt-get update
          sudo apt-get install -y groff
          pip install qrcode[pil]

      - name: Generate man pages HTML and TOC
        run: python scripts/generate_man.py

      - name: Commit and push docs
        run: |
          git config --global user.name "enclov-actions"
          git config --global user.email "actions@github.com"
          git add docs/
          git commit -m "Update man page HTMLs and TOC [skip ci]" || echo "No changes to commit"
          git push origin main
