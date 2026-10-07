// Tests for generated headers.
#include <cassert>
#include <cstring>
#include "sim800_at_persistence_modes/persistence_types.hpp"
#include "sim800_at_persistence_modes/at_basic.hpp"
#include "sim800_at_persistence_modes/sms.hpp"
#include "sim800_at_persistence_modes/at_3gpp.hpp"

int main() {
    using namespace sim800::persistence;

    // at_basic array exists and has entries
    static_assert(AT_BASIC_PERSISTENCE_COUNT > 0, "at_basic must not be empty");
    static_assert(AT_BASIC_PERSISTENCE_COUNT <= MAX_PERSISTENCE_PER_HEADER,
                  "at_basic exceeds MAX_PERSISTENCE_PER_HEADER");

    // sms array exists
    static_assert(SMS_PERSISTENCE_COUNT > 0, "sms must not be empty");

    // FQN lookups
    auto* ipr = sim800::persistence::at_basic::find_at_basic_persistence("AT+IPR", "rate");
    assert(ipr != nullptr);
    assert(ipr->persistence_mode == PersistenceMode::AutoSave);
    assert(ipr->requires_reboot == true);

    auto* cmgf = sim800::persistence::sms::find_sms_persistence("AT+CMGF", "mode");
    assert(cmgf != nullptr);
    assert(cmgf->persistence_mode == PersistenceMode::ExplicitSave);
    assert(cmgf->save_command == "AT&W");

    auto* cmgs = sim800::persistence::sms::find_sms_persistence("AT+CMGS", "da");
    assert(cmgs != nullptr);
    assert(cmgs->persistence_mode == PersistenceMode::Volatile);
    assert(cmgs->is_volatile == true);

    // profile_number: explicit match required
    auto* not_found = sim800::persistence::sms::find_sms_persistence("AT+CMGF", "mode", 0);
    assert(not_found == nullptr); // profile_number is PROFILE_UNSET, not 0

    // at_3gpp shared file
    static_assert(AT_3GPP_PERSISTENCE_COUNT > 0, "at_3gpp must not be empty");

    return 0;
}