# Persistence acceptance coverage

No repository, database, or persistence tests are implemented in the foundation.
This directory reserves the normal-suite location required by
[`contractorcalc-persistence`](../../persistence-design.md).

The storage slice must add real SQLite tests here for the schema, validated
codecs, transactions, close/reopen durability, failures, and clear/write ordering.
An empty directory or passing shell suite is not persistence acceptance.
