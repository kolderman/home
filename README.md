# New Home Build: Youngsville, Louisiana

Plans, studies and models for our new single-level house (plus a bonus room over the garage) and the backyard pond landscape. They started from Melissa's hand-drawn dot-grid sketch (1 dot = 2 ft).

> **This repo is a snapshot** of the Claude project folder taken on 2026-10-30. Draft M edits are still in progress, so the project folder may be newer than this repo. Ask Claude to re-sync it when you want the latest.

## Main documents

Open the `.html` files in a browser. They are self-contained.

| Document | What it is |
|---|---|
| [home-plan/home-floor-plan.html](home-plan/home-floor-plan.html) | **The living floor plan** (draft M): sketch, to-scale blueprint, roof plan, low-voltage plan, upstairs |
| [home-plan/floor-plan-draft-m-markup.pdf](home-plan/floor-plan-draft-m-markup.pdf) | 11x17 markup PDF of draft M for Apple Pencil corrections (K and L PDFs kept as history) |
| [home-plan/floor-plan-review-draft-m.html](home-plan/floor-plan-review-draft-m.html) | Review of draft M (must-fixes and smaller items, all approved) |
| [home-plan/architectural-review-draft-k.html](home-plan/architectural-review-draft-k.html) | Architectural review of draft K (roof, stair and bonus room decisions) |
| [home-plan/blueprint-study.html](home-plan/blueprint-study.html) | Blueprint study: primary suite, great room and guest wing options |
| [home-plan/interior-design-pass.html](home-plan/interior-design-pass.html) | Interior design pass (glass wall, ceilings, kitchen, lounge and so on) |
| [home-plan/floor-plan-design-review.html](home-plan/floor-plan-design-review.html) | Earlier design review |
| [home-plan/floor-plan-proposal-mockup.html](home-plan/floor-plan-proposal-mockup.html) | Proposal mockup |
| [home-plan/landscape-plan.html](home-plan/landscape-plan.html) | Landscape plan, rev. D, centered on the rec pond |
| [home-plan/pond-shape-options.html](home-plan/pond-shape-options.html) | Six new pond shape options (pick pending) |
| [home-plan/long-pond-option.html](home-plan/long-pond-option.html) | Long pond option |
| [home-plan/pond-wetland-study.html](home-plan/pond-wetland-study.html) | Pond wetland filter study |
| [home-plan/house-3d.html](home-plan/house-3d.html) | 3D walkthrough (Three.js). `house-3d-standalone.html` has every asset inlined |
| [home-plan/handoff/HANDOFF.md](home-plan/handoff/HANDOFF.md) | Self-contained brief for handing the design to another AI or designer |

## Folder layout

- `home-plan/` holds everything for the house and landscape.
  - `plan-generator.py`, `roofkit.py`: generate the floor plan page. `draft-l/` and `draft-m/` hold snapshots of the generator.
  - `blueprint-study/`, `review-m/`, `landscape-generator/` and `pond-shapes/` hold the scripts and images behind each study.
  - `house-3d/` holds the 3D model source, textures and stills.
  - `blender/` holds the Blender render package and script (the renders themselves are on the desktop PC).
  - `handoff/` holds the handoff brief and zip.
- `uploads/` holds files we uploaded to the project: the five HEIC photos of the original sketch, screenshots and reference images, and a PDF. File extensions were added so they open here.

## Large files

`home-plan/blender/home-blender-package.zip` (71 MB) and the handoff zip are stored with **Git LFS**, since GitHub rejects single files over 100 MB and warns over 50 MB. They download normally from the GitHub website. To get them with a clone, install Git LFS first (`git lfs install`).

## Not in this repo (yet)

The chat history and the project memory (the running list of decisions) live in the Claude project itself. Claude can export either one to Markdown and add it here on request.
