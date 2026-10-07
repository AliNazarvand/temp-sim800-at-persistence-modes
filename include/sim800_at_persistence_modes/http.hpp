// ============================================================
// AUTO-GENERATED FILE - DO NOT EDIT MANUALLY
// Generated from: data/http.yaml
// Content hash (SHA-256 of entries section only): 80d501d8e597fa75
// Generator: scripts/generate_headers.py
// Generator version: 1.0.0
// YAML schema version: 1.0.0
// Database version: 1.0.0
// To regenerate: cmake --build . --target generate
// ============================================================

#pragma once
#include "persistence_types.hpp"
#include "database_version.hpp"
#include <array>
#include <cstddef>
#include <string_view>

namespace sim800::persistence::http {

inline constexpr std::array<PersistenceEntry, 2> HTTP_PERSISTENCE = {{
    PersistenceEntry{
        "AT+HTTPPARA",
        "cid",
        PROFILE_UNSET,
        Category::Http,
        PersistenceMode::Volatile,
        std::string_view{},
        SaveScope::NotApplicable,
        std::string_view{},
        PowerLossBehavior::Lost,
        ResetBehavior::ResetToDefault,
        FactoryResetBehavior::Retained,
        false,
        true,
        false,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Chapter 8, Section AT+HTTPPARA",
        ExtractionStatus::NotSpecified,
        PresenceStatus::Present,
        "V1.12",
        std::array<std::string_view, MAX_AVAILABLE_VERSIONS>{{
            "V1.01",
            "V1.10",
            "V1.12",
            std::string_view{},
            std::string_view{},
            std::string_view{},
            std::string_view{},
            std::string_view{},
        }},
        3,
        std::array<VersionEntry, MAX_VERSION_SPECIFIC>{{
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        }},
        0,
        260,
        "CID is a per-session parameter; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+HTTPPARA",
        "url",
        PROFILE_UNSET,
        Category::Http,
        PersistenceMode::Volatile,
        std::string_view{},
        SaveScope::NotApplicable,
        std::string_view{},
        PowerLossBehavior::Lost,
        ResetBehavior::ResetToDefault,
        FactoryResetBehavior::Retained,
        false,
        true,
        false,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Chapter 8, Section AT+HTTPPARA",
        ExtractionStatus::NotSpecified,
        PresenceStatus::Present,
        "V1.12",
        std::array<std::string_view, MAX_AVAILABLE_VERSIONS>{{
            "V1.01",
            "V1.10",
            "V1.12",
            std::string_view{},
            std::string_view{},
            std::string_view{},
            std::string_view{},
            std::string_view{},
        }},
        3,
        std::array<VersionEntry, MAX_VERSION_SPECIFIC>{{
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        VERSION_ENTRY_PAD,
        }},
        0,
        260,
        "URL parameter is per-session; inferred from AT command manual."
    },
}};

inline constexpr std::size_t HTTP_PERSISTENCE_COUNT = HTTP_PERSISTENCE.size();
static_assert(HTTP_PERSISTENCE_COUNT <= MAX_PERSISTENCE_PER_HEADER,
              "HTTP_PERSISTENCE count exceeds MAX_PERSISTENCE_PER_HEADER");

inline const PersistenceEntry* find_http_persistence(std::string_view command,
                                                         std::string_view param_name,
                                                         std::uint8_t profile_number = PROFILE_UNSET) noexcept {
    for (std::size_t i = 0; i < HTTP_PERSISTENCE_COUNT; ++i) {
        if (HTTP_PERSISTENCE[i].command == command
            && HTTP_PERSISTENCE[i].parameter_name == param_name
            && HTTP_PERSISTENCE[i].profile_number == profile_number) {
            return &HTTP_PERSISTENCE[i];
        }
    }
    return nullptr;
}

} // namespace sim800::persistence::http
