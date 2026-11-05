---
name: terraform
description: Terraform work. Load for any Terraform task, including editing .tf or .tfvars files, HCL, modules, providers, state, plans, or running terraform or opentofu commands.
---

# Terraform

Terraform is declarative: configuration describes desired state, not procedural logic.

Because of this, tests are rarely useful or needed.
Do not add tests for Terraform configuration unless the user explicitly asks for them.

Strive to keep Terraform declarative.
\`for_each\`\`, etc. is fine but prefer "duplicate" declarative code over opaque procedural code.
Terraform was not really designed for procedural logic; it was only added as a necessity and so should only be used as a necessity.
