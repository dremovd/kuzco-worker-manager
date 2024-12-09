# kuzco-worker-manager
Helper script to run multiple workers with CLI

Don't forget to install kuzco before start:
```bash
curl -fsSL https://kuzco.xyz/install.sh | sh
```

# Simple setup & run (you need to change worker command)

```bash
git clone https://github.com/dremovd/kuzco-worker-manager; cd kuzco-worker-manager
git pull; curl -fsSL https://kuzco.xyz/install.sh | sh; python run_kuzco_workers.py "kuzco worker start --worker V6hwT4-ptyfw25dcg8JwB --code 53877007-c01b-4389-9b8f-3e6aebe90f2e" 10 --silent
```



# Usage examples:
```bash
python3 run_kuzco_workers.py "kuzco worker start --worker V6hwT4-ptyfw25dcg8JwB --code 53877007-c01b-4389-9b8f-3e6aebe90f2e" 3
```

```bash
cmd=
python run_kuzco_workers.py "${cmd}" 1 --silent
```

OR for silent run:
```bash
python3 run_kuzco_workers.py "kuzco worker start --worker V6hwT4-ptyfw25dcg8JwB --code 53877007-c01b-4389-9b8f-3e6aebe90f2e" 3 --silent
```

# Parameters:
```
--no-inference-timeout 10
# This parameter will set timeout for a worker to 10 minutes (default is 60)

--silent
# This will remove all workers output, which leaves only manager own logs
```
