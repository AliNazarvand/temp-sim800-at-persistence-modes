// ============================================================
// AUTO-GENERATED FILE - DO NOT EDIT MANUALLY
// Generated from: data/audio.yaml
// Content hash (SHA-256 of entries section only): 9ba31e6d6fba9347
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

namespace sim800::persistence::audio {

inline constexpr std::array<PersistenceEntry, 4> AUDIO_PERSISTENCE = {{
    PersistenceEntry{
        "AT+CLVL",
        "level",
        PROFILE_UNSET,
        Category::Audio,
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
        "Chapter 10, Section AT+CLVL",
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
        312,
        "Loudspeaker volume level; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+CMIC",
        "gain",
        PROFILE_UNSET,
        Category::Audio,
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
        "Chapter 10, Section AT+CMIC",
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
        310,
        "Microphone gain; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+CMUT",
        "mute",
        PROFILE_UNSET,
        Category::Audio,
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
        "Chapter 10, Section AT+CMUT",
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
        314,
        "Microphone mute state is per-call; inferred from AT command manual."
    },
    PersistenceEntry{
        "AT+CRSL",
        "level",
        PROFILE_UNSET,
        Category::Audio,
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
        "Chapter 10, Section AT+CRSL",
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
        313,
        "Ringer sound level; inferred from AT command manual."
    },
}};

inline constexpr std::size_t AUDIO_PERSISTENCE_COUNT = AUDIO_PERSISTENCE.size();
static_assert(AUDIO_PERSISTENCE_COUNT <= MAX_PERSISTENCE_PER_HEADER,
              "AUDIO_PERSISTENCE count exceeds MAX_PERSISTENCE_PER_HEADER");

inline const PersistenceEntry* find_audio_persistence(std::string_view command,
                                                         std::string_view param_name,
                                                         std::uint8_t profile_number = PROFILE_UNSET) noexcept {
    for (std::size_t i = 0; i < AUDIO_PERSISTENCE_COUNT; ++i) {
        if (AUDIO_PERSISTENCE[i].command == command
            && AUDIO_PERSISTENCE[i].parameter_name == param_name
            && AUDIO_PERSISTENCE[i].profile_number == profile_number) {
            return &AUDIO_PERSISTENCE[i];
        }
    }
    return nullptr;
}

} // namespace sim800::persistence::audio
