# kuzco-worker-manager
Helper script to run multiple workers with CLI

Don't forget to install kuzco before start:
```bash
curl -fsSL https://kuzco.xyz/install.sh | sh
```

# Simple setup & run (you need to change worker command)

```bash
git clone https://github.com/dremovd/kuzco-worker-manager; cd kuzco-worker-manager
git pull; curl -fsSL https://kuzco.xyz/install.sh | sh; python run_kuzco_workers.py "kuzco worker start --worker V6hwT4-ptyfw25dcg8JwB --code 53877007-c01b-4389-9b8f-3e6aebe90f2e" 10
```

# Usage examples:
```bash
python run_kuzco_workers.py "kuzco worker start --worker V6hwT4-ptyfw25dcg8JwB --code 53877007-c01b-4389-9b8f-3e6aebe90f2e" 3
```
OR for silent run:
```bash
python run_kuzco_workers.py "kuzco worker start --worker V6hwT4-ptyfw25dcg8JwB --code 53877007-c01b-4389-9b8f-3e6aebe90f2e" 3 --silent
```
