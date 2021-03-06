# neighborhood

Server, CLI, and library that can turn an SF street address into an SF district and neighborhood.

To regenerate the data, download the ["Street Data Extract" data set](https://sfelections.org/tools/election_data/dataset.php?ATAB=d1970-01-01) and
run:

```bash
cd data
./join_data.py elections-data.txt precincts.tsv > ../src/data/neighborhood_data.tsv
```

Note that if the elections data set adds precincts, these must be manually added to precincts.tsv.

This can be run on the command line via:

```bash
. .venv/bin/activate
./src/find_neighborhood.py "123 Main St"
```

This can be run as a server locally (hot reload) via:

```bash
make run
```

And accessed via:

<http://localhost:8080/?address=123+Main+St>

This can be run as a Docker container:

```bash
make run_docker
```
