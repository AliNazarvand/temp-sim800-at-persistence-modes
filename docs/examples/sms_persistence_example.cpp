// Self-contained example: SMS PersistenceEntry.
#include <cassert>
#include "sim800_at_persistence_modes/persistence_types.hpp"
#include "sim800_at_persistence_modes/sms.hpp"

int main() {
    using namespace sim800::persistence;
    constexpr PersistenceEntry ve{
        "AT+CMGF", "mode", PROFILE_UNSET,
        Category::Sms, PersistenceMode::ExplicitSave,
        "AT&W", SaveScope::BothProfiles,
        std::string_view{},
        PowerLossBehavior::Retained, ResetBehavior::ResetToProfile,
        FactoryResetBehavior::ResetToFactoryDefault,
        false, false, false,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Chapter 5, Section AT+CMGF",
        ExtractionStatus::ExtractedFromText, PresenceStatus::Present,
        "V1.12",
        {"V1.01", "V1.10", "V1.12"}, 3,
        {}, 0,
        145,
        "AT&W saves to active profile."
    };
    assert(ve.command == "AT+CMGF");
    assert(ve.persistence_mode == PersistenceMode::ExplicitSave);
    assert(ve.save_command == "AT&W");
    return 0;
}