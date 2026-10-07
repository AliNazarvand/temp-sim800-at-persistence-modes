// Tests that doc examples compile and run.
#include <cassert>
#include "sim800_at_persistence_modes/persistence_types.hpp"

int main() {
    using namespace sim800::persistence;
    constexpr PersistenceEntry e{
        "AT+TEST", "param", PROFILE_UNSET,
        Category::AtBasic, PersistenceMode::Unknown,
        std::string_view{}, SaveScope::NotApplicable,
        std::string_view{},
        PowerLossBehavior::Unknown, ResetBehavior::Unknown,
        FactoryResetBehavior::Unknown,
        false, false, false,
        "doc", "section",
        ExtractionStatus::NotSpecified, PresenceStatus::Present,
        "V1.12",
        {"V1.12"}, 1,
        {}, 0,
        PAGE_UNSET,
        "test"
    };
    assert(e.command == "AT+TEST");
    assert(e.persistence_mode == PersistenceMode::Unknown);
    return 0;
}