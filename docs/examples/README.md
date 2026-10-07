# Examples

## find_*_persistence signature

Generated headers expose:

```cpp
const PersistenceEntry* find_<category>_persistence(
    std::string_view command,
    std::string_view param_name,
    std::uint8_t profile_number = PROFILE_UNSET) noexcept;
```

For entries with an explicit `profile_number` (e.g. `AT+CMGF` with
`profile_number=0`), you **must** pass the same value explicitly:

```cpp
auto* e = find_sms_persistence("AT+CMGF", "mode", 0);
```

## Self-contained examples

Examples in this directory build a `PersistenceEntry` object in place and
assert on its structure. They do **not** depend on live `data/*.yaml`.