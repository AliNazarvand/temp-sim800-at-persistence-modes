// Self-contained example: build a basic AT PersistenceEntry in place.
#include <cassert>
#include <cstdint>
#include <string_view>
#include "sim800_at_persistence_modes/persistence_types.hpp"
#include "sim800_at_persistence_modes/at_basic.hpp"

int main() {
    using namespace sim800::persistence;
    // Self-contained object: no dependency on live data.
    constexpr PersistenceEntry ve{
        "AT+IPR", "rate", PROFILE_UNSET,
        Category::AtBasic, PersistenceMode::AutoSave,
        std::string_view{}, SaveScope::NotApplicable,
        std::string_view{},
        PowerLossBehavior::Retained, ResetBehavior::Retained,
        FactoryResetBehavior::Retained,
        true, false, false,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Chapter 2, Section AT+IPR",
        ExtractionStatus::ExtractedFromText, PresenceStatus::Present,
        "V1.12",
        {"V1.01", "V1.10", "V1.12"}, 3,
        {}, 0,
        PAGE_UNSET,
        "Baud rate auto-saved."
    };
    assert(ve.command == "AT+IPR");
    assert(ve.persistence_mode == PersistenceMode::AutoSave);
    assert(ve.requires_reboot);
    return 0;
}