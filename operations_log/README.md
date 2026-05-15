# Operations Log

This directory holds the operational record of decisions, gate closures, discipline events, and protocol additions across Cycle 2 substrate work.

## Entry conventions

- **Filename format:** `YYYY-MM-DD_topic.md`. Date is the date of the event, not the date of writing.
- **Authorship:** Entries are drafted by AI partners in collaboration with Mike, with the drafting partner noted at the bottom of each entry.
- **Honest record principle:** Entries reflect the operational record at the time of writing, including failures, miscalibrations, and corrections. Entries are not curated history. When a later entry corrects an earlier one, both stay in the log — the earlier entry is not retroactively edited.
- **Discipline notes:** Many entries include explicit notes on what the discipline structure caught and what it missed. These are part of the record, not editorial commentary.

## Cross-references

- **Substrate Spec v1.1:** `../flights/flight_6/Flight6_Substrate_Specification_v1.1.md.pdf`
- **Architectural reviews:** `../protocols/architectural_reviews/`
- **Onboarding primers:** `../protocols/onboarding/`

## Standing rules (current as of 14 May 2026)

Five standing rules apply across all AI partners and all inference modes:

1. **No past-tense verbs for unexecuted actions on Mike's machine.** Acceptable forms: "The script to run is...", "Drafted for execution:", "Pending your run:", "Once you execute, expected output is..."
2. **No synthetic telemetry tables.** If a run hasn't happened, the table stays blank. Analytical predictions explicitly labeled as such are acceptable; emulated measurements formatted as data are not.
3. **Execution-verification at parity moments.** When an AI partner reports running code, the architectural review explicitly includes execution-status verification, not just primitive/vocabulary compliance.
4. **Asymmetric execution channel acknowledgment.** Mike is the only AI partner with an execution channel on the production machine. AI-partner-reported "results" are either tool-call outputs in their sandboxed environments (clearly labeled) or predictions/analyses about what Mike's execution would produce.
5. **Gate-closing artifacts route to all reviewing AIs.** Substantive working exchanges happen between Mike and one AI partner at a time. At every gate closure, the actual textual artifacts (terminal outputs, hash values, completion-verification reports, implementation files) route to all reviewing AIs before the next gate opens.
