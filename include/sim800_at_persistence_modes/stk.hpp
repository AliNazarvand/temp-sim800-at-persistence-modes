// ============================================================
// AUTO-GENERATED FILE - DO NOT EDIT MANUALLY
// Generated from: data/stk.yaml
// Content hash (SHA-256 of entries section only): ef4c5521c87cd236
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

namespace sim800::persistence::stk {

inline constexpr std::array<PersistenceEntry, 4> STK_PERSISTENCE = {{
    PersistenceEntry{
        "AT+STKC",
        "cmd",
        PROFILE_UNSET,
        Category::Stk,
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
        "Chapter 11, Section AT+STKC",
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
        344,
        "STK command response is per-session; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+STKEN",
        "enable",
        PROFILE_UNSET,
        Category::Stk,
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
        "Chapter 11, Section AT+STKEN",
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
        340,
        "STK enable state; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+STKR",
        "r",
        PROFILE_UNSET,
        Category::Stk,
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
        "Chapter 11, Section AT+STKR",
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
        342,
        "STK result response is per-session; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+STKTR",
        "tr",
        PROFILE_UNSET,
        Category::Stk,
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
        "Chapter 11, Section AT+STKTR",
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
        346,
        "STK terminal response is per-session; inferred from AT command manual."
    },
}};

inline constexpr std::size_t STK_PERSISTENCE_COUNT = STK_PERSISTENCE.size();
static_assert(STK_PERSISTENCE_COUNT <= MAX_PERSISTENCE_PER_HEADER,
              "STK_PERSISTENCE count exceeds MAX_PERSISTENCE_PER_HEADER");

inline const PersistenceEntry* find_stk_persistence(std::string_view command,
                                                         std::string_view param_name,
                                                         std::uint8_t profile_number = PROFILE_UNSET) noexcept {
    for (std::size_t i = 0; i < STK_PERSISTENCE_COUNT; ++i) {
        if (STK_PERSISTENCE[i].command == command
            && STK_PERSISTENCE[i].parameter_name == param_name
            && STK_PERSISTENCE[i].profile_number == profile_number) {
            return &STK_PERSISTENCE[i];
        }
    }
    return nullptr;
}

} // namespace sim800::persistence::stk
