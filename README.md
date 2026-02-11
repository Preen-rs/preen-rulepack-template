# preen-rulepack (Template)

This folder is the base template for building Preen rulepacks.

## Workflows

- `Validate Rulepack (PR/Main)`: validates rulepack files on PRs and `main`.
- `Release Rulepack`: one-click release flow (version bump + signing + tag + release).

## Quick Start

1. Copy this folder into a new repository (recommended name: `preen-rulepack-<topic>`).
2. Replace placeholders in `manifest.toml`:
   - `{{PACK_ID}}`
   - `{{PACK_NAME}}`
   - `{{PACK_VERSION}}`
   - `{{PACK_DESCRIPTION}}`
   - `{{AUTHOR}}`
   - `{{HOMEPAGE}}`
   - `{{OS_TARGET}}` (`Macos` or `Linux`)
   - `{{SIGNING_IDENTITY}}` (recommended default: `https://github.com/<org>/<repo>/.github/workflows/release-manual.yml@refs/heads/main`)
3. Add or edit rules in `rules/`.
4. Push to `main`.

## Validate locally

```bash
python3 scripts/validate_pack.py
```

## Release (Recommended)

1. Run `Release Rulepack` and set `version` to `x.x.x`.
2. Wait for a green run.
3. Verify from Preen:
   - `preen plugin preflight <git-url>@<tag>`
   - `preen plugin test <git-url>@<tag>`
   - `preen plugin install <git-url>@<tag>`

The manual release workflow enforces:
- valid semver input
- unique tag
- signature artifacts (`manifest.sig`, `manifest.cert`)
- matching tag and manifest version
- GitHub release asset upload (`manifest.toml`, `manifest.sig`, `manifest.cert`, `manifest.ci.sig`, `manifest.ci.pem`)

## Plugin Author Checklist

1. Keep rules small, focused, and idempotent.
2. Keep requested capabilities minimal.
3. Run local validation before opening PR.
4. Use `Release Rulepack` for every release.
5. Verify preflight/test/install against the newly created tag.

See `CONTRIBUTING.md` for the full authoring and release policy.

## Required files

- `manifest.toml`
- `manifest.sig`
- `manifest.cert`
- `rules/*.toml`
