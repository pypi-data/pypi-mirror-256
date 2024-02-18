rm -rf dist

# python3 -m pip install --upgrade build twine
python3 -m build
python3 -m twine upload --repository pypi dist/* --non-interactive -p pypi-AgEIcHlwaS5vcmcCJDE0NGUyZTE4LWFmZDQtNGNkMS1iM2ZkLWRiN2M1MzAwNjczNgACKlszLCJhMGVlMDYzNi1kOGFlLTQ2MDEtYTlmZC1lMDRmMjIzY2RlMGYiXQAABiC73TR5NF1BKWvgWVUMe_1fVAFvjvzBM9PB5fn8IW7NTQ