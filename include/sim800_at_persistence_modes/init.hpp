// ============================================================
// AUTO-GENERATED FILE - DO NOT EDIT MANUALLY
// Generated from: data/init.yaml
// Content hash (SHA-256 of entries section only): e38288dcb56eae84
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

namespace sim800::persistence::init {

inline constexpr std::array<PersistenceEntry, 2> INIT_PERSISTENCE = {{
    PersistenceEntry{
        "AT+CFUN",
        "fun",
        PROFILE_UNSET,
        Category::Init,
        PersistenceMode::ExplicitSave,
        "AT&W",
        SaveScope::BothProfiles,
        std::string_view{},
        PowerLossBehavior::Retained,
        ResetBehavior::ResetToProfile,
        FactoryResetBehavior::ResetToFactoryDefault,
        false,
        false,
        false,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Chapter 1, Section AT+CFUN",
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
        25,
        "Functionality level; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+CPAS",
        "status",
        PROFILE_UNSET,
        Category::Init,
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
        "Chapter 1, Section AT+CPAS",
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
        27,
        "Activity status is runtime only; inferred from AT command manual."
    },
}};

inline constexpr std::size_t INIT_PERSISTENCE_COUNT = INIT_PERSISTENCE.size();
static_assert(INIT_PERSISTENCE_COUNT <= MAX_PERSISTENCE_PER_HEADER,
              "INIT_PERSISTENCE count exceeds MAX_PERSISTENCE_PER_HEADER");

inline const PersistenceEntry* find_init_persistence(std::string_view command,
                                                         std::string_view param_name,
                                                         std::uint8_t profile_number = PROFILE_UNSET) noexcept {
    for (std::size_t i = 0; i < INIT_PERSISTENCE_COUNT; ++i) {
        if (INIT_PERSISTENCE[i].command == command
            && INIT_PERSISTENCE[i].parameter_name == param_name
            && INIT_PERSISTENCE[i].profile_number == profile_number) {
            return &INIT_PERSISTENCE[i];
        }
    }
    return nullptr;
}

} // namespace sim800::persistence::init
