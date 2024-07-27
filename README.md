# kuzco-worker-manager
Helper script to run multiple workers with CLI

Don't forget to install kuzco before start:
```bash
curl -fsSL https://kuzco.xyz/install.sh | sh
```

# Usage examples:
```bash
python run_kuzco_workers.py "kuzco worker start --worker V6hwT4-ptyfw25dcg8JwB --code 53877007-c01b-4389-9b8f-3e6aebe90f2e" 3
```
OR for silent run:
```bash
python run_kuzco_workers.py "kuzco worker start --worker V6hwT4-ptyfw25dcg8JwB --code 53877007-c01b-4389-9b8f-3e6aebe90f2e" 3 --silent
```
