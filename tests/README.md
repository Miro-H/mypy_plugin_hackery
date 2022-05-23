# Plugin Tests

TODO

## Forward Reference

> When testing your plugin, you should have a test case that forces a module top level to be processed multiple times. The easiest way to do this is to include a forward reference to a class in a top-level annotation. Example:
```
c: C  # Forward reference causes second analysis pass
class C: pass
```