---
name: requirement-levels
description: "Use when writing, interpreting, or reviewing requirement levels in specifications, policies, API contracts, or agent instructions. Apply RFC 2119 meanings for MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY, including their synonyms and RFC 8174's capitalization clarification."
---

# Requirement Levels (RFC 2119)

Use requirement keywords to distinguish absolute requirements, recommendations with valid exceptions, and optional behavior.
This skill summarizes [RFC 2119](https://www.rfc-editor.org/info/rfc2119/), with the capitalization clarification from [RFC 8174](https://www.rfc-editor.org/info/rfc8174/).
Together, these RFCs form BCP 14.

## Keyword Meanings

| Keywords | Meaning |
| --- | --- |
| MUST, REQUIRED, SHALL | An absolute requirement of the specification. |
| MUST NOT, SHALL NOT | An absolute prohibition of the specification. |
| SHOULD, RECOMMENDED | A recommendation that can have valid exceptions in particular circumstances. Understand and carefully weigh the full implications before choosing another course. |
| SHOULD NOT, NOT RECOMMENDED | A recommendation against behavior that can be acceptable or useful in particular circumstances. Understand and carefully weigh the full implications before choosing that behavior. |
| MAY, OPTIONAL | A truly optional item. Implementations can include or omit it. |

Synonyms within each row have the same requirement level.
Prefer MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY for consistent wording within a document.
This preference is a writing convention, not an additional RFC requirement.

### Optional Features and Interoperability

Under RFC 2119, an implementation that omits an option MUST interoperate with an implementation that includes it, possibly with reduced functionality.
An implementation that includes an option MUST interoperate with one that omits it, except for the functionality that the option provides.
MAY does not mean that peers can assume support for an optional feature.

## Capitalization and Scope

Under RFC 8174, these keywords have their special BCP 14 meanings only when they appear in all capitals.
Lowercase or mixed-case words retain their normal English meanings.
Do not conclude that text is non-normative merely because it lacks uppercase keywords.
Normative requirements can exist without these keywords.

Check the document's stated conventions before interpreting or editing its requirements.
Do not silently apply BCP 14 to unrelated prose or replace an explicitly defined local convention.
RFC 2119 also notes that the force of these words depends on the requirement level of the containing document.
These keywords do not change the priority of an agent instruction or override higher-priority instructions.

When a document adopts BCP 14, place the following declaration near its beginning.
The wording below comes from RFC 8174:

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119](https://www.rfc-editor.org/rfc/rfc2119) [RFC8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they appear in all capitals, as shown here.

Include references to both RFCs when using this declaration.

## Choose a Requirement Level

1. Identify the actor, required behavior, and conditions under which the statement applies.
1. Use MUST or MUST NOT when the requirement or prohibition is absolute within those conditions.
1. Use SHOULD or SHOULD NOT when valid exceptions can exist, but the full implications need careful consideration.
1. Use MAY when inclusion and omission are both permitted without an exceptional justification.
1. State relevant consequences, especially security implications of violating requirements or recommendations.
1. Check related statements for contradictions and inconsistent terminology.

Use these imperatives with care and sparingly.
RFC 2119 section 6 limits their use to interoperability needs or behavior that could cause harm.
Do not impose an implementation method when interoperability does not require that method.
If a project adopts this vocabulary for broader policies or agent instructions, make that local scope explicit.
Do not present that broader use as an IETF requirement.

Make requirements specific enough to check.
State explicit conditions rather than weakening a conditional obligation to SHOULD.
For example, “If authentication is enabled, the server MUST reject invalid credentials” remains absolute when its condition holds.

## Examples

These examples illustrate keyword selection, not additional requirements from the RFCs.

| Intent | Example |
| --- | --- |
| Absolute obligation | The server MUST reject requests with invalid authentication credentials. |
| Absolute prohibition | The client MUST NOT send credentials over an unencrypted connection. |
| Recommendation with valid exceptions | The client SHOULD retry transient failures with exponential backoff. |
| Recommendation against behavior | The client SHOULD NOT retry a non-idempotent request without evidence that the first attempt failed before execution. |
| Optional feature | The server MAY support response compression. |

For recommendations, explain known exceptions and their consequences when that context is available.
Do not invent exceptions or rationales that the source does not provide.

## Review and Rewrite Checklist

- Preserve the original requirement level when rewriting.
- Do not replace MUST with SHOULD to make an instruction sound polite.
- Do not replace SHOULD with MUST merely to make prose stronger.
- Do not interpret MAY as a recommendation or an obligation.
- Do not treat SHOULD as an absolute obligation or as unrestricted permission to ignore the recommendation.
- Distinguish permission from possibility: “The request might fail” describes possibility, not a MAY-level option.
- Preserve the actor, conditions, exceptions, and scope of each requirement.
- Flag unclear intent instead of silently selecting a stronger or weaker keyword.
- Explain security consequences when deviations could cause harm.
- Keep descriptive explanations separate from normative requirements.

When asked to rewrite text, return the revised text and flag unresolved ambiguity.
When asked to review text, identify the statement, explain the mismatch, and propose wording that preserves its intended force.

## Sources

- [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/info/rfc2119/) — definitions, interoperability, restrained use, and security considerations.
- [RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/info/rfc8174/) — capitalization rules and the updated declaration.
