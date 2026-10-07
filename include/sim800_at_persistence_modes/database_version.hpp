// include/sim800_at_persistence_modes/database_version.hpp
#pragma once
#include <string_view>
namespace sim800::persistence {
inline constexpr std::string_view DATABASE_VERSION    = "1.0.0";
inline constexpr std::string_view YAML_SCHEMA_VERSION = "1.0.0";
inline constexpr std::string_view GENERATOR_VERSION   = "1.0.0";
} // namespace sim800::persistence