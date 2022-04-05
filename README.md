# vps_backup_utils

Backup Utilities for Linux VPS with MySQL and other data

## develop

### install dependencies

```
poetry install
```

### test on host machine (not recommended)

```
poetry run pytest
```

### test on docker (recommended)

```
docker-compose up -d mysql postgresql
docker-compose up pytest --build
```

### build & publish

```
poetry install
poetry build
poetry publish
```