# Sources manifest

Provenance record for content bundled in **Craftline** (`craftline`), formerly UIUX Abhishek DevKit and UIUX Abhishek Design. Third-party files remain the work of their authors under the licenses shown; original project content is listed separately at the end. See [NOTICE.md](NOTICE.md).

## Upstream sources

| Source | Author | License | Bundled version | Bundled path |
| --- | --- | --- | --- | --- |
| [Impeccable](https://github.com/pbakaus/impeccable) | Paul Bakaus | Apache-2.0 + [NOTICE](LICENSES/IMPECCABLE_NOTICE.md) | 4.1.1 (upstream front matter); exact commit not recorded | `references/impeccable/` (40 Markdown files) |
| [platform-design-skills](https://github.com/ehmo/platform-design-skills) | ehmo | MIT | Derived content within Impeccable 4.1.1 | `references/impeccable/reference/ios.md`, `android.md` |
| [Apple Design](https://github.com/emilkowalski/skills) | Emil Kowalski | MIT | Exact commit not recorded | `references/apple-design/` (1 Markdown file) |

The initial import came from locally installed copies of Impeccable and Apple Design. Local home-directory paths are intentionally left out. Each original entry-point `SKILL.md` was renamed to `SOURCE_SKILL.md`, and other Markdown documents keep their relative locations. Executable scripts, binaries and non-Markdown assets were excluded, so full upstream tooling is not reproduced.

## License and notice files

| File | Source | Retrieved |
| --- | --- | --- |
| `LICENSES/IMPECCABLE_APACHE-2.0.txt` | Impeccable `LICENSE` | Initial import |
| `LICENSES/IMPECCABLE_NOTICE.md` | Impeccable `NOTICE.md` at commit `3e38e595c708` | 2026-11-03 |
| `LICENSES/PLATFORM_DESIGN_SKILLS_MIT.txt` | platform-design-skills `LICENSE` (`main`) | 2026-11-03 |
| `LICENSES/APPLE_DESIGN_MIT.txt` | emilkowalski/skills license | Initial import |

The same files are mirrored in `plugin/skills/craftline/LICENSES/` so they travel with installed copies.

## Included third-party files (SHA-256)

Paths are relative to `plugin/skills/craftline/references/`.

All files below stay in the repository and in Skills CLI installs. The release ZIPs (Claude Chat upload and Claude Code plugin), built by `tools/package_skill.py`, leave out the nine "Never load" files from `SKILL.md`: `impeccable/reference/live.md`, `live-setup.md`, `hooks.md`, `doctor.md`, `visualize.md`, `routing.md`, `init.md`, `craft.md` and `degraded/` (four files). They only drive Impeccable tooling that isn't bundled. Shipping a subset of an Apache-2.0 work is permitted (Section 4), and every ZIP keeps `LICENSE`, `NOTICE.md` and `LICENSES/`, including Impeccable's NOTICE.

**Modified file (Apache-2.0 §4(b)):** `impeccable/SOURCE_SKILL.md`. On 2026-11-24 Abhishek Rampal modified `SOURCE_SKILL.md` for Craftline: he removed its YAML front matter (`name`, `description`, `version`, `user-invocable`, `argument-hint`, `license` and `allowed-tools`, which only serve Impeccable's own tooling and whose tool wildcards the Claude plugin directory refused) and replaced it with a one-line attribution note. The body text is unchanged. Its checksum below is of the modified file.

- `apple-design/SOURCE_SKILL.md  77bb63b7043bb93aca2ff4ab040c249484eef35682bb6ff7163433c31d30adc7`
- `impeccable/SOURCE_SKILL.md  dc4f3e74fff0d0dfd0ed6987cc206a16e43e5567b7aecff201ef2262710906e0`
- `impeccable/reference/adapt.md  ec58806f16fc7ba29bccef08f2e158cd00be077ce05d45e943a59bd26dc6dc55`
- `impeccable/reference/adapt.native.md  17c583cf8ad41266ea1e787b666b9d91fe13469d3d0f6af57c08e0146f9b17ac`
- `impeccable/reference/android.md  058f81f256134841875fd3183e06b37a023de0c877fd2b9eecd97011640791fe`
- `impeccable/reference/animate.md  94b4ce6299fea93d9f256b2d25705961a76bc5ea940c56db4145686ebc99df1b`
- `impeccable/reference/audit.md  57402ef6fd9d0745f8c60d778f77da83a8b16edf751fa1013598a0f6e5f0f541`
- `impeccable/reference/audit.native.md  010ecb4ef79d6e063280791cd2d5e6a689f4f7a3d66c60d7d43f04e7b2067966`
- `impeccable/reference/bolder.md  4879f38b23d0a251a63cbb0327e660296194cd2e71eb4da3236c6ebfe5807746`
- `impeccable/reference/clarify.md  6c382f8283756e8a693d832b750f7e4cbff1ca5bdcc3825b2b4ef4da9f21876a`
- `impeccable/reference/colorize.md  d1fbd55074abb2251bdaa03749d34acc42c38e46e47549f18f5848df57d43c42`
- `impeccable/reference/craft-floor.md  96e2e6bd4fcf9a2c6da65fb029f96d9176308fae2efd9d8653d3b8d838960e07`
- `impeccable/reference/craft.md  9205e222bc6565b37fb504ceec93233c2d2a456802b69d16e6b1c44723907c4c`
- `impeccable/reference/critique.md  75f47b538e00bd40d67b2fd6d2ea2f024b20748386e683e76a26f53e6576365c`
- `impeccable/reference/degraded/asset-producer.md  df8eb799aa2038f7255f0fa565ab4ae037270313c7dc25167113e7955c9e7f64`
- `impeccable/reference/degraded/documenter.md  97a09e350c383cb2f6bba027b83bedffd12a23b1b439ad4a045a48953eb19365`
- `impeccable/reference/degraded/finish-reviewer.md  c70d4bd77fe9142bbe7e3b412d3ca44443e0914bdb323577dc2acb59e8d72078`
- `impeccable/reference/degraded/manual-edit-applier.md  9aae8d5bfb72a8cf3473dca74d5046e28002c0b43a7f9b3c14cd0f1a06c8deb4`
- `impeccable/reference/delight.md  56500b1f9d2fcec8324d7f448d813048b5831a46d3feeb1055bd3eb17ec3660f`
- `impeccable/reference/distill.md  b2f60e0154bf0e687badc46d8c8420e2118a9a6e21162050722be779dc02cb6d`
- `impeccable/reference/doctor.md  916a54e3b198d227f5e1322fe5cd9e13c7a2d4e11a6884f66fcb31377d86f8ed`
- `impeccable/reference/document.md  87b3db688c7963898bda8096f7868fed05ec5a0a80d14298e8b906b70cdf9c42`
- `impeccable/reference/extract.md  bfc51972fbf387566dc9e29c8b1af479a66ab401fdbce659fae9e6a5a9d85316`
- `impeccable/reference/harden.md  8a1c872773996dfa1c1eb765ac7ed8e8d41f99d4f12f090b4725b694e85eaa62`
- `impeccable/reference/hooks.md  fb0d664a41ffccdd923e4f9beef5a335100cb37ca02283d2ac41f0c7c862e831`
- `impeccable/reference/init.md  d7b4254e9b40857deafcd8194e4e7c55f6009c06d92899f1f0df697d8999900c`
- `impeccable/reference/ios.md  40c87038b5f75147a5952a96237acf312a327bf70c1bcd8e0a5f064625ae9668`
- `impeccable/reference/layout.md  54e66bfb19d5d7b8d9feb7e05384ae2aa2432b9788355501f288d2575646fe98`
- `impeccable/reference/live-setup.md  e3728926aab72ad980272587b31dabd60f7592c4a1ceeb96d4ef7f1ca4824bcd`
- `impeccable/reference/live.md  ab4d9040e9f37b1aef1f22319593280c7d2ba5a442e0d9eb12a8097bbbc505fe`
- `impeccable/reference/new-work.md  b57dc5dc24acfbb448e7f014d228fad0623b90cd25e41097f55f0d35076555f5`
- `impeccable/reference/onboard.md  9a2c08ee2516d2ee87129e7ebe6a0895f9990c9852d1f6fa7e70be9a6a88a659`
- `impeccable/reference/operate.md  a9d2203acd45ca33a13d5c68b02b23ed512425ac15f0e8438318ed124b43729d`
- `impeccable/reference/optimize.md  6d368b679a0ed1815812815de65863b5840d419589dfbda06224c01149240287`
- `impeccable/reference/overdrive.md  a9856cb40da6519b1334bcfc75a4fbe83bef39ca86ee6f3effcb2a96794c627c`
- `impeccable/reference/polish.md  ec8139122245d0b71f078c4960b9abec72bbca80f46db04e83323593416018fe`
- `impeccable/reference/quieter.md  ee6d6d127c1c2ab3526d529a8e3698be2185b5e346ac617f37501de2c0698b97`
- `impeccable/reference/routing.md  534a8653a4bd9f0d437eca1b4bf807f9adca1a7d584d38cf8bb161d3ef7fdffc`
- `impeccable/reference/shape.md  a55f016c046cb6a27c55bd7f346375aeb506a755c4fbca19a5f92dbd42309c23`
- `impeccable/reference/typeset.md  2031c995a3d4b4f1c74535c055ca21ac133034ced477905da543b714802adc10`
- `impeccable/reference/visualize.md  5f25be0799f7936b900443ed515fe58827fcb966dd92ab5f5edef0119f8f62c2`

## Original project content

| Content | Origin | License |
| --- | --- | --- |
| `references/frontend/` (9 guides), `references/workflows/` (2 guides), `templates/` (2 templates) | *UIUX Abhishek Design Frontend Engineering Expansion* pack (named after the project's former name), supplied by the maintainer on 2026-11-03 (`uiuxabhishek-frontend-expansion.zip`, SHA-256 `4a86b38a1efa79b8dfd0760eec70ff2ba2e53b80c9b417a869525c7521a83db1`) | MIT (© Abhishek Rampal) |
| `references/workflows/git-workflow.md`, `references/workflows/git-recovery-and-release.md` | Universal Git & Repository Workflow, written for this project on 2026-11-04 (no third-party text) | MIT (© Abhishek Rampal) |
| `references/adapters/impeccable-without-cli.md` | Manual substitutes for Impeccable's unbundled script steps, written for this project on 2026-11-24 (no third-party text) | MIT (© Abhishek Rampal) |
| `references/frontend/forms.md`, `security.md`, `seo-and-metadata.md`, `figma-to-code.md`, `cross-platform-native.md` | Frontend capability guides written for this project on 2026-11-24 (no third-party text) | MIT (© Abhishek Rampal) |
| `references/workflows/ticket-delivery.md`, `templates/ticket-delivery-report.md` | Provider-neutral ticket lifecycle and report, split out of `azure-devops-delivery.md` and generalized from `ado-delivery-report.md` on 2026-11-24 | MIT (© Abhishek Rampal) |
| `references/workflows/agent-plans.md` | Head-only rules for planning and dispatching Claude Code agents, moved out of SKILL.md §5 on 2026-11-24 | MIT (© Abhishek Rampal) |
| `references/craftforce/` (15 playbooks), `plugin/agents/task-implementer.md`, `plugin/agents/spec-reviewer.md`, `plugin/agents/session-diagnostician.md` | Craftforce process layer (brainstorm → worktree → plan → agent or inline execution with review → verified finish, plus debugging, review handling, parallel agents, skill writing and session diagnosis), written for this project on 2026-11-24 from the maintainer's outline of the 15 capabilities (no third-party text). The outline's session-start hook and browser visual companion were deliberately not built (Markdown only) | MIT (© Abhishek Rampal) |
| `plugin/agents/` (agent files), `plugin/README.md`, `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | Claude Code plugin agents, directory README and manifests written for this project on 2026-11-24 (no third-party text) | MIT (© Abhishek Rampal) |

The pack describes itself as framework-independent guides written for this project, with application-specific files from an earlier private archive excluded. It contains no third-party text, source code, URLs or credentials. Changes made during integration:

- Removed stack- and domain-specific identifiers (named framework/library stack, a fixed `development` branch, domain-specific tenancy terms).
- Removed duplicated gate and review steps from `azure-devops-delivery.md` in favor of links to `testing.md` and `review-and-release.md`; `review-and-release.md` now points to `templates/pr-description.md`.
- Converted cross-references to relative Markdown links.
- 2026-11-04: moved the generic Git preflight, staging, commit and push steps of `azure-devops-delivery.md` into the shared `git-workflow.md`, which ADO now links to; the Azure-specific ticket, PR and comment steps are unchanged.
- 2026-11-05 (2.0.1): `git-workflow.md` and `azure-devops-delivery.md` no longer fetch or write refs in `audit`, `plan` or ADO dry runs, and they honor "don't fetch" and "offline" in every mode.
- 2026-11-24 (2.1.0): the provider-neutral lifecycle moved from `azure-devops-delivery.md` to `ticket-delivery.md`, which now also covers GitHub Issues, Jira and Linear; the ADO file keeps only Azure specifics. `templates/ado-delivery-report.md` became `templates/ticket-delivery-report.md`.
- Not imported: the pack's `PACKAGE_MANIFEST.json`, `README.md` and `integration/` instructions (installer metadata, merged into `SKILL.md` routing instead).

Checksums (paths relative to `plugin/skills/craftline/`):

- `references/adapters/impeccable-without-cli.md  13232107300aeadcc051fecbcc8dae8c84d483c0c3b15ca2cf3385b599d01571`
- `references/craftforce/brainstorming.md  5b5b192cdb17d2605ea9d3ea82858569068f93c0ee39cf81e3947dcbae735258`
- `references/craftforce/diagnosing-craftforce.md  798841e33aba2e7a66373bbc249835a92e9eef368017adeaf60a5a263dc3d30a`
- `references/craftforce/dispatching-parallel-agents.md  d564e483d4562fe82800c4fea7d85e4278c24aba8ae6dbc08a49dafaa4ea4aae`
- `references/craftforce/executing-plans.md  a9a7c1aae49a0d1fedec3561032e40d7f0a6f47c0d0ed0c89cab52eea38c7298`
- `references/craftforce/finishing-a-development-branch.md  35a3bef60992922ffdf2175b65e2da635b586fc2cb32acbf68ebfeffdefac5b5`
- `references/craftforce/receiving-code-review.md  0112397e7fe261d63c110fd22817c150bfad69ba94325a080221f189ede2345f`
- `references/craftforce/requesting-code-review.md  34b4a1030b1ab23247d7945ec77aaa4d747f8b5c5a6371f0a4326def6c29b841`
- `references/craftforce/subagent-driven-development.md  ce271ac6a11c6232aae205c70a54eb4fe8724bd10665748c8008c44b8d53eb96`
- `references/craftforce/systematic-debugging.md  373643b8c9648e837c44665e54c30d61610b0baaf98d6b0f7478b50bca9e4957`
- `references/craftforce/test-driven-development.md  6ebbf74b191929601aeb5f4f1bbdcf81d418c1c1827fbe9ac83962f4422c4eaf`
- `references/craftforce/using-craftforce.md  53f0c6821ef6279e0152d6141a74c44653bc7691bb7265fbd663894dd2fff355`
- `references/craftforce/using-git-worktrees.md  a314d878032866d6af7e4a683c95dd940e5b207d5851d1611afd935e0991c8c3`
- `references/craftforce/verification-before-completion.md  6092220badc76f9e52c5e5716d7269fc59bb36845e252d1d21af049340250789`
- `references/craftforce/writing-plans.md  47727e26395f55cfaeb99d1b274e044e212e7efa80952a5a15a134043c2a617f`
- `references/craftforce/writing-skills.md  56ef7c43b299e79eda6c22cad97721e43ceb4ebe6e02825e3d6ca8435637f835`
- `references/frontend/admin-crud.md  d5eb94fb9a001761a8daf6c2c73f289f3443666ed2382a6057655e9c1c6c080c`
- `references/frontend/api-integration.md  34a6fc614750eba44ca81d02be6fc935ea8265407e3b297353b4ec19f69f0c62`
- `references/frontend/cross-platform-native.md  44a75bd6184e557f6974af45939fc2bc3862fe8ca0977153136f768d5ce89281`
- `references/frontend/data-reports.md  94b2384676ebedb857082cc98368c33b611dfbb23486a4dba10a0ab2b5d65288`
- `references/frontend/figma-to-code.md  1d82e982d6693e1945b386cc3cdd57ec4c559e04d5192db42e41e838912f1453`
- `references/frontend/forms.md  4e8b6cd9b2a9cfcc88a1eb6bd0962ce570e1201ca5434cca28528ac78cd18519`
- `references/frontend/microfrontends.md  f79ec3983f518d5eb362920085fe80c4f5fe981ce5a9344f3e57d5410fcfb2e6`
- `references/frontend/packages-and-components.md  61de77a4bb3a530cdb3bc6c2303b47586263f10f6f2c9630bd7820face798333`
- `references/frontend/pages-and-routing.md  7ed8444d1806de55ca813cbee015abcaea873a421d4190dc9a835aecaaa2d2a5`
- `references/frontend/review-and-release.md  9cb7ad4de9c7e80cb3c8680901a612e7c7600d8c19940be7200fc7ca53e166dc`
- `references/frontend/security.md  3f7e6b09457d1a3b04796277da8a9718f624e01d9c24fbcb5b6ee68d7c175d45`
- `references/frontend/seo-and-metadata.md  d96ded2de837551a4c5d5da8d9785e850d116e3215aa6ac647d69c9014ff0ddf`
- `references/frontend/state-management.md  812d5717a212bb62bb231fd0268240e9741548ca6bc55a169fc95ea90d66e858`
- `references/frontend/testing.md  a64e9fe97d8de875a9dce02ad22cbfbdc647b59a7286200d709cf3ec00d6498c`
- `references/workflows/ado-configuration.md  ff8cce8c406c5be539aa4af69301f4508c14dc6a306d0ef13713d626868464ac`
- `references/workflows/agent-plans.md  9ec196f3c21a857bf3b6e435b011622c2663c770137485a1b6529098cc7bfda9`
- `references/workflows/azure-devops-delivery.md  5c43d9edb1416222bb3a0c17644273cb8d3da72ef6265c240c6baf1807a0d7bb`
- `references/workflows/git-recovery-and-release.md  360437c2addb9c9a9759cea5fc007e741fe2cf618ca52eca5495d935c6b1ddda`
- `references/workflows/git-workflow.md  a581debca4a298fb45e65b73cdc47507d2b665d32bb4fe22ad09633e63e53d10`
- `references/workflows/ticket-delivery.md  7a8425cacc821082db3f01ee57210b39c8cf2291b4aa808a0a2d7051172d8095`
- `templates/pr-description.md  ed01966273e1e72cdc6c76c8d93a63060fdb3fb8b1e4a0ae0bfd1ab0fa9d3b94`
- `templates/ticket-delivery-report.md  e13d9e63036843bba0696325f184812d7301a211ad5b34becfe3aac132528b87`

Plugin agent files (paths relative to `plugin/`):

- `agents/code-reviewer.md  bce58a3583c0d2314c7a57c93885703bec03f06f22009d03cdc0c8f4272df5cc`
- `agents/delivery-agent.md  0fb07b1078ab3de237c2d07ad6a8fe711de329cadbd16fe7c05eb4d77d1bf468`
- `agents/design-auditor.md  099481bd6f4a4306710ad71a646d46463168e0d40e61837880bb6a7d029dea0d`
- `agents/figma-translator.md  a1e43172d3f6b39296d7fe27ac139dbdd02b9a5ecac78621c93fc9a2254d9b71`
- `agents/frontend-engineer.md  0bcef591c9076979c19d7f079404ce8a4ccb102c06737dbfe9a0234c10c7d62a`
- `agents/session-diagnostician.md  0f60b5192cec00a37b8310e5ed6a689bb93251ac883281d0371be48da13023de`
- `agents/spec-reviewer.md  8f8c3027f632b49453a360a5c8984131e750eac7fbe12e6accd193e9e50e76e9`
- `agents/task-implementer.md  8f1489752b7ab965d621a971467c9ba39126b8cd80ef8dcc2f9706011854cb80`
- `agents/test-engineer.md  b06b0a3989e2c0e4f9362bdabee47170fb3aa7de79707b71a6437ee702fcb973`
- `agents/ui-designer.md  b747fdb31a98abae3cdfe776cc44c5122947891f076d9b88941901224d3f6a92`
- `agents/ux-designer.md  ba9deaad18820d81d01cfec75ca50edf40ba4d1b29e11446702fb5f7b4a6427d`

Plugin icon (path relative to `plugin/`; the Craftline logo, a 1254×1254 PNG supplied by the maintainer on 2026-11-24; no third-party source):

- `.claude-plugin/icon.png  c30e3abde88d746f043a79948a758223f6b1501dfad742368e2b5d8c0811f764`
