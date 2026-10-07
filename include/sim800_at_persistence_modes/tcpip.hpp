// ============================================================
// AUTO-GENERATED FILE - DO NOT EDIT MANUALLY
// Generated from: data/tcpip.yaml
// Content hash (SHA-256 of entries section only): 94c1bedcb2140243
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

namespace sim800::persistence::tcpip {

inline constexpr std::array<PersistenceEntry, 6> TCPIP_PERSISTENCE = {{
    PersistenceEntry{
        "AT+CIPCCFG",
        "nmRetry",
        PROFILE_UNSET,
        Category::Tcpip,
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
        "Chapter 7, Section AT+CIPCCFG",
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
        230,
        "Transparent mode config; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+CIPMODE",
        "mode",
        PROFILE_UNSET,
        Category::Tcpip,
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
        "Chapter 7, Section AT+CIPMODE",
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
        224,
        "Transparent transmission mode; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+CIPMUX",
        "mode",
        PROFILE_UNSET,
        Category::Tcpip,
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
        "Chapter 7, Section AT+CIPMUX",
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
        220,
        "TCP/IP multiplexing mode; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+CIPQSEND",
        "mode",
        PROFILE_UNSET,
        Category::Tcpip,
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
        "Chapter 7, Section AT+CIPQSEND",
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
        228,
        "Send mode selection; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+CIPRXGET",
        "mode",
        PROFILE_UNSET,
        Category::Tcpip,
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
        "Chapter 7, Section AT+CIPRXGET",
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
        232,
        "Receive data mode; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+CIPSTATUS",
        "status",
        PROFILE_UNSET,
        Category::Tcpip,
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
        "Chapter 7, Section AT+CIPSTATUS",
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
        222,
        "Connection status is runtime only; inferred from AT command manual."
    },
}};

inline constexpr std::size_t TCPIP_PERSISTENCE_COUNT = TCPIP_PERSISTENCE.size();
static_assert(TCPIP_PERSISTENCE_COUNT <= MAX_PERSISTENCE_PER_HEADER,
              "TCPIP_PERSISTENCE count exceeds MAX_PERSISTENCE_PER_HEADER");

inline const PersistenceEntry* find_tcpip_persistence(std::string_view command,
                                                         std::string_view param_name,
                                                         std::uint8_t profile_number = PROFILE_UNSET) noexcept {
    for (std::size_t i = 0; i < TCPIP_PERSISTENCE_COUNT; ++i) {
        if (TCPIP_PERSISTENCE[i].command == command
            && TCPIP_PERSISTENCE[i].parameter_name == param_name
            && TCPIP_PERSISTENCE[i].profile_number == profile_number) {
            return &TCPIP_PERSISTENCE[i];
        }
    }
    return nullptr;
}

} // namespace sim800::persistence::tcpip
