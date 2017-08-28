### Description

This program creates an API endpoint that returns a filtered list of
job applicants (candidates) from the set of provided data.

Create an API endpoint that returns a filtered list of job applicants
(candidates) from the set of provided data.

Example API request:

```
GET /candidate?expertise=technical&location=NYC
{
  “type”: “candidate_list”,
  “data”: [{
    “id”: 0,
    “first”: "Bark”,
    “last”: “Ruffalo”,
    “expertise”: “technical”,
    “location”: “NYC”
  }, {
    “id”: 1,
    “first”: “J.K.”,
    “last”: “Growling”,
    “expertise”: “technical”,
    “location”: “NYC”
  }]  
}
```

The API endpoint should allow candidates to be filtered by both expertise and
location via URL query parameters. The endpoint should return candidates sorted
alphabetically by last name.  


### Dependencies

Dependencies can be installed by running `pip install -r requirements.txt`.

The program's dependencies are Python 3+ (tested using Python 3.6.2), `psycopg2`,
Flask and a few associated packages (`flask-restless` and `flask_sqlalchemy`),
`requests`, and `json`.

Regarding other dependencies, it's assumed you have PostgreSQL installed on your
system. The program was tested using PostgreSQL 9.6.4.

### Setup

PostgresSQL must be configured on your system in order for the program to run.
Please follow your OS-specific instructions for this (in my case, I used the
[Arch Wiki](https://wiki.archlinux.org/index.php/PostgreSQL)).

It is assumed that your Postgres password is saved on your system as an environment
variable called `$POSTGRES_PASSWORD`.

### Running

Navigate to the root directory and open two terminal windows. In one, run
`python server.py`. You should see the following output:

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 644-360-566
```

In the other terminal window, run `python client.py`. The output in the `server.py`
window should now be as follows:

```
127.0.0.1 - - [27/Aug/2017 23:01:00] "GET /api/candidates HTTP/1.1" 200 -
127.0.0.1 - - [27/Aug/2017 23:01:00] "GET /api/candidates?filter%5Bobjects%5D=%5B%7B%22or%22%3A+%5B%7B%22name%22%3A+%22expertise%22%2C+%22op%22%3A+%22eq%22%2C+%22val%22%3A+%22product%22%7D%2C+%7B%22name%22%3A+%22location%22%2C+%22op%22%3A+%22eq%22%2C+%22val%22%3A+%22SF%22%7D%5D%7D%5D HTTP/1.1" 200 -
```

And in the `client.py` window:

```
{'num_results': 1727, 'objects': [{'expertise': 'business', 'first_name': 'Mildred', 'last_name': 'Brown', 'location': 'SF'}], 'page': 1, 'total_pages': 173}
{'num_results': 1727, 'objects': [{'expertise': 'business', 'first_name': 'Mildred', 'last_name': 'Brown', 'location': 'SF'}], 'page': 1, 'total_pages': 173}
{'num_results': 1727, 'objects': [{'expertise': 'business', 'first_name': 'Mildred', 'last_name': 'Brown', 'location': 'SF'}], 'page': 1, 'total_pages': 173}
```


### Progress/Completion of Requirements

- [x] Return JSON.
However, the id field needs to be added (should it be the primary key?) and the JSON needs
to be formatted as in the example output under `Description` above. The `to_json()`
method in `server.py` should help with this.
- [ ] Allow candidates to be filtered with any combination of the expertise and
location fields.
Currently, the program allows filtering based on expertise and location, but the
results returned are incomplete and/or incorrect. For example, as we saw above:

```
get("technical", "NYC")
get("business", "SF")
get("product", "SF")
```

returns the following three times, ignoring the technical NYC candidates and product SF candidate.

```
{'num_results': 1617, 'objects': [{'expertise': 'business', 'first_name': 'Mildred', 'last_name': 'Brown', 'location': 'SF'}], 'page': 1, 'total_pages': 162}
```

- [x] Use a SQL based datastore (SQLite is okay)
- [x] Initially populate the datastore with the data from the provided CSV file.
(Another error to fix is that the database is re-populated each time - it should
only update with new contents.)
- [x] Be written in Python.
(Next steps: Check `pylint`, `flake8`,  `autopep8` conformance. Implement docstrings and
unit tests).
- [ ] Deploy to Heroku.
