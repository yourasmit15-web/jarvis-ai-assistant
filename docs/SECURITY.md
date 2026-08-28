# Security Notes

- No hard-coded credentials.
- Permissions are denied by default except safe web search.
- Tool execution is guarded by permission checks.
- Level 2/3 operations require confirmation records.
- Memory storage blocks secret-like content (`password`, `token`, `secret`, `private key`).
- Audit log captures permission checks, tool execution, confirmations, and emergency stop.
