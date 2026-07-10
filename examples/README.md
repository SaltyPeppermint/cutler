### cutler examples

```
$ cutler hello_world.ncl
$ cutler nice.ncl -v tmpdir=/tmp -v out=./foo.mp4
$ mkdir abba
$ cutler -j 4 abba.ncl -v tmpdir=/tmp -v outdir=./abba --records-from-csv abba.csv
```

In the above examples, replace `cutler` by either `nix run '.#default' --` or `uv run` by your choice.
