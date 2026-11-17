# Waterwear Field Console

One screen for wearable physiology, evoked-potential checks and imaging worklists for people who have opted in. Everything shown here is simulated demo data.

## Roster

Select a person to see their consented signals. People without active consent show no data.

| ID | Zone | Consent | Heart rate | Stress | Device | State |
| --- | --- | --- | --- | --- | --- | --- |

**No one selected.** Choose a row above.

## Activity log

Console ready.

## Management instructions

1. **Enroll people first.** Each person signs a plain-language consent form that lists every signal collected (heart rate, skin temperature, evoked-potential tests, imaging reports), who can see it, and how long it is kept. They can withdraw in the app at any time, and withdrawal stops collection immediately.
2. **Assign roles.** Operators see de-identified trends. Clinicians see named results for people in their care. Admins manage access but cannot read signals. Use single sign-on with multi-factor, and issue short-lived tokens instead of shared passwords.
3. **Collect the minimum.** Set a retention period for each signal type (for example 30 days for raw heart rate, longer for signed clinical reports). Delete automatically when the period ends.
4. **Keep humans in charge of actions.** The assistant may summarize, flag and suggest. A named person must approve any dispatch, and the approval is logged with their name and time.
5. **Treat evoked-potential and imaging data as medical records.** Store them in a clinical system that meets your local health-privacy rules (HIPAA in the US), keep only a link and a status on this console, and let a licensed clinician interpret results.
6. **Review the audit log weekly.** Look for unusual lookups, off-hours access and exports. Report each finding to the data-protection owner.
7. **Never use these signals for discipline, hiring or pay decisions.** Use them for safety and care only.

## Build notes for your engineers

- Bind servers to `127.0.0.1` behind a TLS reverse proxy. Do not expose `0.0.0.0` without authentication.
- Check consent inside every MCP tool and resource, and return nothing when consent is off.
- Split tools into read-only and action tools. Action tools such as dispatch create a pending request that a human approves.
- Write an append-only audit entry for every tool call, including the model's reasoning summary and the approving user.
- Treat text inside telemetry fields as untrusted data so it cannot instruct the model.
- Fix a bug in the sample code: `self.active_connections in self.active_connections and ...remove()` should be an `if` check.