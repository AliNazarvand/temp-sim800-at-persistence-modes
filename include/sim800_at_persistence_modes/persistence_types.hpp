// include/sim800_at_persistence_modes/persistence_types.hpp
#pragma once
#include <cstddef>
#include <cstdint>
#include <string_view>
#include <array>

namespace sim800::persistence {

using page_t = std::uint32_t;
inline constexpr page_t PAGE_UNSET = 0xFFFFFFFFu;
inline constexpr std::uint8_t PROFILE_UNSET = 0xFFu;

inline constexpr std::size_t MAX_AVAILABLE_VERSIONS     = 8;
inline constexpr std::size_t MAX_VERSION_SPECIFIC       = 8;
inline constexpr std::size_t MAX_PERSISTENCE_PER_HEADER = 256;

enum class Category : std::uint8_t {
    AtBasic, At3gpp27007, At3gpp27005, Sms, Gprs, Tcpip,
    Http, Ftp, Audio, Stk, Init,
    NotApplicable
};

enum class PersistenceMode : std::uint8_t {
    AutoSave, ExplicitSave, Volatile, FactoryLocked,
    ProfileSpecific, Conditional, Unknown, MomentaryAction,
    NotApplicable
};

enum class SaveScope : std::uint8_t {
    Profile0, Profile1, BothProfiles, FactoryOnly, NotApplicable
};

enum class PowerLossBehavior : std::uint8_t {
    Retained, Lost, ResetToDefault, Unknown,
    NotApplicable
};

enum class ResetBehavior : std::uint8_t {
    Retained, ResetToDefault, ResetToProfile, Unknown,
    NotApplicable
};

enum class FactoryResetBehavior : std::uint8_t {
    ResetToFactoryDefault, Retained, Unknown,
    NotApplicable
};

enum class ExtractionStatus : std::uint8_t {
    ExtractedFromTable, ExtractedFromText, NotSpecified
};

enum class PresenceStatus : std::uint8_t {
    Present, ExplicitlyRemoved, NotMentioned,
    NotApplicable
};

struct VersionEntry {
    std::string_view version;

    bool persistence_mode_same_as_representative;
    PersistenceMode persistence_mode;

    bool save_command_same_as_representative;
    std::string_view save_command;

    bool save_scope_same_as_representative;
    SaveScope save_scope;

    bool profile_number_same_as_representative;
    std::uint8_t profile_number;

    bool power_loss_behavior_same_as_representative;
    PowerLossBehavior power_loss_behavior;

    bool reset_behavior_same_as_representative;
    ResetBehavior reset_behavior;

    bool factory_reset_behavior_same_as_representative;
    FactoryResetBehavior factory_reset_behavior;

    bool requires_reboot_same_as_representative;
    bool requires_reboot;

    bool is_volatile_same_as_representative;
    bool is_volatile;

    bool is_factory_locked_same_as_representative;
    bool is_factory_locked;

    PresenceStatus presence_status;
    ExtractionStatus extraction_status;

    bool source_document_same_as_representative;
    std::string_view source_document;

    bool source_section_same_as_representative;
    std::string_view source_section;

    bool page_hint_same_as_representative;
    page_t page_hint;
};

inline constexpr VersionEntry VERSION_ENTRY_PAD{
    std::string_view{},
    true, PersistenceMode::NotApplicable,
    true, std::string_view{},
    true, SaveScope::NotApplicable,
    true, PROFILE_UNSET,
    true, PowerLossBehavior::NotApplicable,
    true, ResetBehavior::NotApplicable,
    true, FactoryResetBehavior::NotApplicable,
    true, false,
    true, false,
    true, false,
    PresenceStatus::NotApplicable, ExtractionStatus::NotSpecified,
    true, std::string_view{},
    true, std::string_view{},
    true, PAGE_UNSET
};

struct PersistenceEntry {
    std::string_view command;
    std::string_view parameter_name;
    std::uint8_t profile_number;
    Category category;
    PersistenceMode persistence_mode;
    std::string_view save_command;
    SaveScope save_scope;
    std::string_view nvram_address;
    PowerLossBehavior power_loss_behavior;
    ResetBehavior reset_behavior;
    FactoryResetBehavior factory_reset_behavior;
    bool requires_reboot;
    bool is_volatile;
    bool is_factory_locked;
    std::string_view source_document;
    std::string_view source_section;
    ExtractionStatus extraction_status_latest;
    PresenceStatus presence_status_latest;
    std::string_view representative_version;
    std::array<std::string_view, MAX_AVAILABLE_VERSIONS> available_in_versions;
    std::uint8_t available_in_versions_count;
    std::array<VersionEntry, MAX_VERSION_SPECIFIC> version_specific;
    std::uint8_t version_specific_count;
    page_t page_hint;
    std::string_view notes;
};

constexpr bool operator==(const VersionEntry& a, const VersionEntry& b) noexcept {
    if (a.version != b.version) return false;
    if (a.persistence_mode_same_as_representative != b.persistence_mode_same_as_representative) return false;
    if (a.persistence_mode != b.persistence_mode) return false;
    if (a.save_command_same_as_representative != b.save_command_same_as_representative) return false;
    if (a.save_command != b.save_command) return false;
    if (a.save_scope_same_as_representative != b.save_scope_same_as_representative) return false;
    if (a.save_scope != b.save_scope) return false;
    if (a.profile_number_same_as_representative != b.profile_number_same_as_representative) return false;
    if (a.profile_number != b.profile_number) return false;
    if (a.power_loss_behavior_same_as_representative != b.power_loss_behavior_same_as_representative) return false;
    if (a.power_loss_behavior != b.power_loss_behavior) return false;
    if (a.reset_behavior_same_as_representative != b.reset_behavior_same_as_representative) return false;
    if (a.reset_behavior != b.reset_behavior) return false;
    if (a.factory_reset_behavior_same_as_representative != b.factory_reset_behavior_same_as_representative) return false;
    if (a.factory_reset_behavior != b.factory_reset_behavior) return false;
    if (a.requires_reboot_same_as_representative != b.requires_reboot_same_as_representative) return false;
    if (a.requires_reboot != b.requires_reboot) return false;
    if (a.is_volatile_same_as_representative != b.is_volatile_same_as_representative) return false;
    if (a.is_volatile != b.is_volatile) return false;
    if (a.is_factory_locked_same_as_representative != b.is_factory_locked_same_as_representative) return false;
    if (a.is_factory_locked != b.is_factory_locked) return false;
    if (a.presence_status != b.presence_status) return false;
    if (a.extraction_status != b.extraction_status) return false;
    if (a.source_document_same_as_representative != b.source_document_same_as_representative) return false;
    if (a.source_document != b.source_document) return false;
    if (a.source_section_same_as_representative != b.source_section_same_as_representative) return false;
    if (a.source_section != b.source_section) return false;
    if (a.page_hint_same_as_representative != b.page_hint_same_as_representative) return false;
    if (a.page_hint != b.page_hint) return false;
    return true;
}
constexpr bool operator!=(const VersionEntry& a, const VersionEntry& b) noexcept { return !(a == b); }

constexpr bool operator==(const PersistenceEntry& a, const PersistenceEntry& b) noexcept {
    if (a.command != b.command) return false;
    if (a.parameter_name != b.parameter_name) return false;
    if (a.profile_number != b.profile_number) return false;
    if (a.category != b.category) return false;
    if (a.persistence_mode != b.persistence_mode) return false;
    if (a.save_command != b.save_command) return false;
    if (a.save_scope != b.save_scope) return false;
    if (a.nvram_address != b.nvram_address) return false;
    if (a.power_loss_behavior != b.power_loss_behavior) return false;
    if (a.reset_behavior != b.reset_behavior) return false;
    if (a.factory_reset_behavior != b.factory_reset_behavior) return false;
    if (a.requires_reboot != b.requires_reboot) return false;
    if (a.is_volatile != b.is_volatile) return false;
    if (a.is_factory_locked != b.is_factory_locked) return false;
    if (a.source_document != b.source_document) return false;
    if (a.source_section != b.source_section) return false;
    if (a.extraction_status_latest != b.extraction_status_latest) return false;
    if (a.presence_status_latest != b.presence_status_latest) return false;
    if (a.representative_version != b.representative_version) return false;
    if (a.available_in_versions_count != b.available_in_versions_count) return false;
    for (std::uint8_t i = 0; i < a.available_in_versions_count; ++i) {
        if (a.available_in_versions[i] != b.available_in_versions[i]) return false;
    }
    if (a.version_specific_count != b.version_specific_count) return false;
    for (std::uint8_t i = 0; i < a.version_specific_count; ++i) {
        if (!(a.version_specific[i] == b.version_specific[i])) return false;
    }
    if (a.page_hint != b.page_hint) return false;
    if (a.notes != b.notes) return false;
    return true;
}
constexpr bool operator!=(const PersistenceEntry& a, const PersistenceEntry& b) noexcept { return !(a == b); }

} // namespace sim800::persistence