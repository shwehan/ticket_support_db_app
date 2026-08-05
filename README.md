# Lakebase Support App — Day 1 Homework

A deployable Flask app for the Databricks AI Bootcamp homework. It uses the same Lakebase secret convention as the Day 1 boilerplate and stores every ticket and message in Lakebase (Postgres).

## Included requirements

- Related `tickets` and `ticket_messages` tables with a foreign key
- Three seed tickets and two messages per ticket
- View/filter tickets, view messages, create tickets, add messages, and update status
- Bonus: priority, validation, error messages, status filters, statistics, and responsive styling
- Parameterized SQL for user-provided values

## Fastest setup if Day 1 already works

1. Create a new GitHub repository and add this folder's files. Do **not** add `.env` or credentials.
2. In Databricks, create a Git folder pointing to your new repository.
3. Confirm the secret used by Day 1 still exists: scope `database`, key `lakebase-url`. Its value should be the full Lakebase Postgres URL.
4. Ensure the app's service principal can read that secret. If you used the same process as Day 1, repeat the secret permission step for this new app identity.
5. Go to **Compute → Apps → Create app → Custom**, select the Git folder containing `app.py` and `app.yaml`, and deploy.
6. Open the app. On first startup it creates the schema and inserts sample data only if `tickets` is empty.

If your Day 1 app used a different scope or key, change the two values in `app.yaml`—not the secret itself.

## New Lakebase setup (only if you cannot reuse Day 1)

1. In **Catalog → Lakebase**, create or open a database instance.
2. Create a native/password role and copy its Postgres connection URL. The URL normally ends with `?sslmode=require`.
3. Store the full URL in a Databricks secret with scope `database` and key `lakebase-url`, following your Day 1 `setup_secrets.py` workflow.
4. Grant the deployed app identity permission to read the secret and connect to the database.
5. Deploy using the steps above.

Never commit the connection URL, password, `.env`, API keys, or tokens.

## Local development (optional)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Put the Lakebase URL in .env; do not commit it.
python app.py
```

Open `http://localhost:8000`. Local development connects to the same Lakebase database, so use a development database if you do not want to alter the deployed data.

## Verify before submission

Use this checklist in the deployed app:

- [ ] The three sample tickets load.
- [ ] Every sample ticket has two messages.
- [ ] Create a new ticket, then refresh; it remains.
- [ ] Add a message, then refresh; it remains.
- [ ] Change the ticket status, then refresh; it remains.
- [ ] Try a status filter and confirm the statistics.
- [ ] Capture one screenshot of the app.

For the database screenshot, open the Lakebase SQL editor and run:

```sql
SELECT * FROM tickets ORDER BY ticket_id;

SELECT * FROM ticket_messages ORDER BY ticket_id, created_at;
```

Capture the table browser/results showing both table names and sample rows. Do not include the connection URL or credentials in screenshots.

## Submission package

Submit:

1. The Databricks App URL (make sure instructor access is enabled).
2. This source folder as a ZIP.
3. A deployed-app screenshot.
4. A Lakebase tables/sample-data screenshot.
5. A 3–5 sentence reflection.

Example reflection—edit it so it is true to your experience:

> The most difficult part was connecting the deployed app identity securely to Lakebase and confirming that it could read the Databricks secret. Lakebase differs from a traditional analytics table because it is an operational Postgres database designed for low-latency row-level inserts and updates, transactions, and relationships such as foreign keys. Analytics tables are usually optimized for large scans and batch transformations rather than interactive application writes. Next, I would add authentication and assign tickets to specific support agents.

## Troubleshooting

- **App starts, then fails immediately:** inspect app logs; confirm `database/lakebase-url` exists and the app identity can read it.
- **Connection refused/SSL error:** regenerate or recopy the full connection URL and retain `sslmode=require`.
- **Permission denied creating tables:** use a Lakebase role with `CREATE` on the target schema, or have the schema owner run the SQL in `SCHEMA_SQL` once.
- **Existing Day 1 tables are present:** that is fine; this app creates only `tickets`, `ticket_messages`, and one index.
- **Free Edition option missing:** product availability can vary by workspace. Confirm that the same Lakebase instance and Apps features used for Day 1 are still visible before creating anything new.

