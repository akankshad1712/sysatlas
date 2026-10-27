# Capacity Planning

The initial design targets a single local instance and SQLite. Likely constraints are serialized writes, database file growth, collector process startup overhead, and unbounded retention. Before adding distributed components, measure snapshot size, collection duration, write latency, query latency, and concurrent request behavior. Define retention and backup policy before long-running deployment.
