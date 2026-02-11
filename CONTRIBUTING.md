# Contributing

This repository is a template for Preen rulepacks.

## Authoring Rules

- Keep each rule focused on one cleanup intent.
- Prefer idempotent behavior (running multiple times should not cause damage).
- Choose the minimum required capabilities in `manifest.toml`.
- Use descriptive rule IDs and names; IDs should be stable once published.

## Safety and Trust

- Do not request broad capabilities unless strictly required.
- Keep `signing.sigstore = true`.
- Keep `signing.identity` aligned with this repository:
  - `https://github.com/<org>/<repo>/.github/workflows/release-manual.yml@refs/heads/main`
- Never publish unsigned release revisions.

## Validation

Before opening a PR:

```bash
python3 scripts/validate_pack.py
```

On CI:

- `Validate Rulepack (PR/Main)` must pass.

## Releasing

Use the `Release Rulepack` workflow.

Input:

- `version`: semver without `v` prefix (`x.x.x`)

Workflow behavior:

- updates `manifest.toml` version
- updates signing identity for the active workflow
- generates `manifest.sig` and `manifest.cert`
- validates pack files
- commits release state to `main`
- creates and pushes `v<version>` tag
- creates GitHub release with signature artifacts

After release, verify from Preen CLI:

```bash
preen plugin preflight <git-url>@<tag>
preen plugin test <git-url>@<tag>
preen plugin install <git-url>@<tag>
```

## Common Mistakes

- releasing from a local script without CI signing
- changing `pack_id` after publishing
- requesting unnecessary capabilities
- creating a tag manually before signed artifacts are updated
