# Aborted run, not evidence

`runner/run_f18_container.sh development f18 v1.3.6` at commit `1fb6487` (image `565e5547…`, guard status OK).
The D-028 guard change in that commit wrote `image-guard.txt` into the run directory before the runner started, and
`runner/run_f18.py` refuses an evidence directory that is not empty (`IntegrityError: evidence directory is not empty`).
No fixture was run and no result was produced. `broker-output.txt` is the script's terminal output. The guard file is
now written after the runner exits (next commit). Recorded by Claude (Claude Opus 5.5, via Claude Code).
