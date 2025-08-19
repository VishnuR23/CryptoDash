
Optional C++ core with a minimal arbitrage engine.

### Build
```bash
cd cpp-core
cmake -S . -B build && cmake --build build -j
./build/arb_engine < quotes.json
```
> `arb_engine` expects a JSON array of quotes: `[{"exchange":"A","bid":100,"ask":101},{"exchange":"B","bid":102,"ask":103}]`
