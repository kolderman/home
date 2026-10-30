# New Home Build: Design Handoff (Draft K)

**Prepared:** October 26, 2026 · **Owner:** Michael (and his wife, who drew the original sketch)
**Location:** Youngsville, Louisiana (Lafayette Parish, USDA zone 9a)

This package hands the full design to a new designer or AI agent working from scratch. You have no access to the earlier conversation, so everything you need is here or in the files beside this document. Where the brief says **decided**, treat it as fixed. Where it says **open**, you may propose an answer, but label it as your proposal.

---

## 0. What's in this package

| Path | What it is |
|---|---|
| `HANDOFF.md` | This brief. Read it first. |
| `images/01-floor-plan-furnished.png` | Draft K furnished plan (the main reference image). The back of the house (pond side) is at the top. |
| `images/02-floor-plan-blueprint-dimensioned.png` | Draft K to-scale blueprint with dimension strings. One grid square is 2 ft. |
| `images/03-low-voltage-plan.png` | Cameras, Wi-Fi, data drops, speakers, conduit, rack. |
| `images/04-garage-option-A-chosen.png` | The garage as decided. |
| `images/05-…`, `06-…` | The two upstairs (bonus room) options. Still open. |
| `images/10-landscape-site-plan.png` | The whole yard with the house, rev. D. |
| `images/11-pond-detail-numbered.png` | Close-up of the long recreation pond. |
| `images/12-pond-water-loop.png`, `13-pond-section-on-axis.png` | How the pond's water moves, and a section on the main axis. |
| `images/20-entry-view-chosen-A.png` | An interior sketch from the front doors toward the glass wall (chosen look). |
| `images/21-powder-room-option-A-chosen.png` | Powder room vanity, the chosen option. |
| `images/3d-placeholder/*.jpg` | Seven stills (front, dusk, corner, back from the pond, from the fire pit, aerial, dollhouse) from a quick Three.js massing model of draft K. **The exterior style in them is only a placeholder.** Use them to check the massing and the site, not as a style to copy. |
| `sketch-photos/sketch-photo-1…5.jpg` | Photos of the original hand-drawn dot-grid sketch, where one dot is 2 ft. The current plan supersedes them where they differ. |
| `data/plan-data-draft-k.json` | **Machine-readable geometry for every room, wall, door, window, porch, post and low-voltage device.** Use it for CAD and 3D. |
| `data/pond-rev-d.json` | Machine-readable pond, wetland, terrace and feature geometry in the same coordinate system. |
| `reference/*.html` | The original design pages: floor plan, landscape plan, interior design pass and design review. Open them in a browser for the full text. |
| `reference/floor-plan-draft-k-markup.pdf` | 11×17 markup set for draft K. |
| `reference/source/` | The Python generators that drew the plans (`plan-generator.py` holds the floor plan's source data). |

**Precedence when sources disagree:** `data/plan-data-draft-k.json` and `plan-generator.py` come first, then this brief, then the images, then the HTML pages, then the sketch photos.

---

## 1. Coordinate system (read this before anything else)

- Units are **feet**. Coordinates are **wall centerlines**. Exterior walls are 6 in thick, interior walls about 4½ in.
- The plan is viewed from above with the **back of the house (the pond) at the top** and the **street at the bottom**.
- **x** runs from 0 at the outside wall of the bedroom wing to 113 at the garage side wall. Standing at the street facing the house, the bedroom wing and lounge are on your **left** and the garage is on your **right**.
- **y** increases toward the **front/street**. The front porch edge is y = 72, the bedroom 2 back wall is y = 13, and the primary bath's back wall is y = -2.5. **Negative y is the back yard.**
- **Main axis: x = 37.5.** The front doors, the 16 ft glass wall, the sun ledge in the pond and the waterfall all line up on it. This is the most important design idea in the house.
- **North is unknown.** Don't assume an orientation. If you need one for sun studies, state your assumption.

---

## 2. Site

- Several acres in Youngsville, LA. Mostly flat, with nearly unlimited space behind the house. The property continues past every edge of the site plan.
- The lot sits **well above flood elevation**, so no special flood design is needed for the house. The FEMA zone for the pond area hasn't been confirmed yet.
- The groundwater is high and the soil is clay-heavy, which is typical of south Louisiana. The climate is hot and humid, with heavy rain and hurricanes.
- There's no native stone, so all stone is trucked in from Arkansas, Oklahoma or the Texas Hill Country. Use one stone type throughout, such as Arkansas fieldstone or Texas moss rock.
- The drive comes in from the street to the front-facing garage on the right.

---

## 3. The house at a glance

- A **single-level home** with a **bonus floor over the garage** (one or two rooms, still open).
- The overall footprint is about **113 ft wide × 74.5 ft deep**, including the primary bath bump-out.
- Heated main floor: **~4,396 sf**. Garage: **~786 sf**. Porches: **~1,054 sf** (back, front and side). Bonus floor: **~770 sf** before knee walls.
- The layout runs left to right as seen from the street:
  - **Bedroom wing** (bedrooms 2 and 3, baths 2 and 3, server room) at the left rear, with the **lounge** at the front left.
  - The **great room** (living, kitchen, dining) in the middle, with the **front porch** in front and the **back porch** and **outdoor kitchen** behind.
  - The **office**, **powder room**, **stairs** and **scullery** right of the kitchen.
  - The **primary suite** (bedroom, dressing room, bath), **laundry** and **side porch** at the right rear.
  - The **garage** at the front right.

---

## 4. Room program (Draft K)

Sizes are centerline to centerline, rounded. Coordinates are (x1, y1) to (x2, y2), as in the JSON.

| Room | Size | Coordinates | Floor |
|---|---|---|---|
| Bedroom 2 | 24' × 13'10" | (0, 13) to (24, 26.8) | wood |
| Bedroom 2 entry alcove | 4'7" × 4'2" | (19.4, 26.8) to (24, 31) | wood |
| Bath 2 (en suite to bed 2) | 13' × 7'7" | (0, 26.8) to (13, 34.4) | tile |
| Walk-in closet, bed 2 | 6'5" × 4'2" | (13, 26.8) to (19.4, 31) | wood |
| Bedroom hall | 11' × 3'5" | (13, 31) to (24, 34.4) | wood |
| Passage + linen closet (2'×3') | 6'6" × 3'1" | (17.5, 34.4) to (24, 37.5) | wood |
| Bedroom 3 | 17'6" × 12'4" | (0, 34.4) to (17.5, 46.7) | wood |
| Bath 3 (en suite to bed 3) | 11'5" × 7'4" | (0, 46.7) to (11.4, 54) | tile |
| Bed 3 vestibule (4' hall, cabinet at end) | 4'4" × 7'4" | (11.4, 46.7) to (15.7, 54) | wood |
| Server room | 6'6" × 9'2" | (17.5, 37.5) to (24, 46.7) | wood |
| Closet, bed 3 (shelving) | 8'4" × 7'4" | (15.7, 46.7) to (24, 54) | wood |
| Lounge (library) | 17' × 18' | (7, 54) to (24, 72) | wood |
| Living | 28' × 28'6" | (24, 34) to (52, 62.5) | wood |
| Kitchen | 16' × 25' | (52, 34) to (68, 59) | wood |
| Dining (open to the kitchen) | 16' × 12' | (52, 22) to (68, 34) | wood |
| Office (incl. corridor, powder, nook) | 18' × 23' + 7' × 6' desk nook | (68, 5) to (86, 34) | wood |
| Office corridor | 4' × 6' | (68, 28) to (72, 34) | wood |
| Powder room | 7' × 6' | (72, 28) to (79, 34) | tile |
| Main hall | 23' × 4' | (68, 34) to (91, 38) | wood |
| Drop zone strip | 12'6" × 2' | (78.5, 38) to (91, 40) | wood |
| Stairs (U-shaped, up to bonus) | 7'6" × 11'6" | (68, 38) to (75.5, 49.5) | wood |
| Closet under/beside stairs | 3' × 11'6" | (75.5, 38) to (78.5, 49.5) | wood |
| Scullery (was pantry) | 10'6" × 13' | (68, 49.5) to (78.5, 62.5) | tile |
| Primary bath | 20' × 10'6" | (86, -2.5) to (106, 8) | tile |
| Dressing room (was primary closet) | 20' × 8' | (86, 8) to (106, 16) | wood |
| Primary bedroom | 20' × 16' | (86, 16) to (106, 32) | wood |
| Laundry | 15' × 8' | (91, 32) to (106, 40) | tile |
| Garage | 34'6" × 26'6" (notched) | polygon in JSON | concrete |

**Porches and outdoor spaces (all covered, with posts):**
- **Back porch + outdoor kitchen:** polygon (24,20) (46,20) (46,10) (68,10) (68,22) (52,22) (52,34) (24,34). The porch is behind the living room, and the outdoor kitchen is the deeper section behind the dining room and against the office wall.
- **Front porch:** (24, 62.5) to (52, 72), with posts along the front edge.
- **Side porch:** (106, 16) to (112, 40), off the primary bedroom. A dashed line marks a possible screened section.
- **Trash bump-in:** (102.4, 40) to (113, 46.4). An enclosed can area reached from outside.
- **Porch posts:** (24.5,20.5) (29.5,20.5) (45.5,20.5) (46.5,10.5) (57,10.5) (67.5,10.5) (24.5,71.5) (33.7,71.5) (42.3,71.5) (51.5,71.5) (111.5,16.5) (111.5,39.5). The middle back-porch post was **moved to x 29.5** so nothing stands in the glass wall's view.

### Room-by-room detail

**Front entry and living room**
- **Front doors:** a 6 ft pair centered on x = 37.5 in the front wall (y 62.5). There is **no foyer and no coat closet** (decided). You walk straight into the living room.
- **Living room:** a **12 ft ceiling** with exposed **sinker cypress beams about every 4 ft**, running right to the front doors with no lowered entry band. The **media wall with the TV** is on the left wall (x = 24). It has **no fireplace** (decided).
- **Back wall (y = 34): a 16 ft multi-slide glass wall** from x 29.5 to 45.5, steel or bronze-clad wood, about 10 ft tall. Its four panels stack into a pocket in the wall to the left (x 25.1–29.5). Motorized screens and solar shades drop from ceiling pockets.
- **Porch door:** a single door at x 47–50 on the same back wall, kept for everyday use.
- **Lounge doors:** a 6 ft opening to the lounge on the left wall (x = 24, y 55.5–61.5), closed by **steel-and-glass double doors**.
- A potted tree sits near the front door in the entry corner.

**Lounge (front left)**
- It reads as a **library**: about 17 ft wide (that width is **fixed**), with an **11 ft ceiling with shallow coffers** (suggested).
- A **flush gas fireplace insert** is centered on the left wall (x = 7). There's no chimney chase, and no window on that wall.
- **Green-lacquer bookcases** flank the fireplace, with a bar cabinet in one.
- The front wall has **one big ~14 ft window**.
- Furniture: four tub chairs around a round table.

**Kitchen**
- An **11 ft flat plaster ceiling**.
- The **range** is on the right wall (x = 68, the stair wall), **directly behind the island**, under a **tapered plaster hood that runs to the ceiling**, with a marble slab backsplash and a pot filler.
- The **paneled fridge and freezer** are on the same wall, closer to the back.
- The **island is 6 ft wide** and about 10 ft long, running front to back, with a rounded end toward the dining room. Stools sit on the living-room side and at the round end. The island was shifted toward the living room so there's a **48 in aisle** to the range.
- The **sink** is on the front wall (y = 59) under a window, **centered between two dishwashers**.
- A **grocery hatch** (not a door) connects the garage to the scullery.

**Dining**
- A **round table** with six chairs (his wife likes round tables) and an 11 ft ceiling.
- A **pair of French doors** in the back wall (x 57.5–62.5) opens to the outdoor kitchen, and there's a window on the left wall.
- A **glass-front wine wall** stands on the right wall in place of a buffet.

**Scullery (was the pantry)**
- A working scullery: sink with a **second dishwasher**, coffee and beverage station, appliance garage, a steam or speed oven, and open shelves with a zellige backsplash.
- There's no door to the garage, only the grocery hatch. The scullery is open to the kitchen.

**Stairs and hall**
- A **U-shaped stair**: two 3 ft runs of 8 treads each and a 3'6" landing at the front. You go up the left run from the hall.
- **One large closet** fills the space under the right run and landing plus the 3 ft strip beside it, with a door from the hall. The goal is to maximize storage.
- A **drop zone** (bench, cubbies, hooks) sits just left of the garage-to-hall door, near the primary suite.
- His wife plans to redraw the stairs and the bedroom wing, so treat their exact shape as provisional.

**Office (right of the dining room, behind the stairs)**
- You reach it through a door off the main hall, **directly across from the stairs**, into a short corridor. The **powder room** opens off the corridor, and the **office door** is at the end of it.
- Inside: an **L-shaped couch** along the back wall whose return butts into **Michael's computer desk** (an L desk on the right wall). They face a **big OLED TV on the left wall**, the porch/dining side, with built-in cabinetry there.
- A **7' × 6' desk nook** holds a U-shaped desk with shelving above.
- Three windows sit on the back wall. **No second window** goes on the porch-side wall, because the TV goes there (decided).
- **It is NOT a theater room** (decided). It stays an office with a couch and a big TV.
- **Sound isolation on all four walls:** double or staggered studs, mineral wool and two layers of ⅝" drywall with damping compound. Add a solid-core door with seals, an insulated ceiling on resilient channel, and lined ducts.
- A **10 ft ceiling** with acoustic plaster (suggested).

**Powder room**
- **Option A (decided):** a furniture-style **cypress vanity** with an **undermount sink in honed marble**, a round brass mirror, two sconces and grasscloth walls. **No vessel sinks** (his wife dislikes them). She picks the final wall finish.
- The toilet and vanity are on the right wall, with shelves open to the corridor.

**Primary suite (right rear)**
- **Primary bedroom** (20' × 16'): entered from the end of the main hall. A **sliding door** (x = 106, y 20–28) opens to the side porch. An **11 ft tray ceiling with cove light** (suggested).
- **Dressing room** (was the closet): **glass-front wardrobes** on both long walls with integrated lighting, a full-length mirror on the end wall and a bench in the aisle. There's no closet island.
- **Primary bath:**
  - A **rectangular tub** under the back window (the primary garden outside lines up on this window).
  - A **WC room** with the toilet on the left wall and shelves open to the bath.
  - A **shower** (6' × 5') in the far corner with a **cased opening, no door**.
  - **Three sinks**, with a wall between the vanities.
  - **No wet room** (decided).
- **Laundry:** the washer and dryer are on the far wall, and a door leads out to the side porch and trash area. The **wall it shares with the primary bedroom is sound-isolated**.

**Bedroom wing (left)**
- These are reached from the living room through an opening on the left wall (x = 24, y 34.9–37.2) into a short passage with a 2'×3' **linen closet**.
- **Bedroom 2:** entered through an alcove. It has a walk-in closet and **bath 2 en suite**: a full-length shower and tub on the outside wall, with the toilet beside the sink on the wall shared with bedroom 3. There is **no outside door from bath 2** (decided).
- **Bedroom 3:** 17'6" × 12'4", option A (decided). A TV built-in sits on its right wall. A **4 ft vestibule** leads to **bath 3** (left, full-depth shower on the outside wall) and a **shelved closet** (right).
- **Server room:** a network rack with its own mini-split. The **electrical panels and the broadband/fiber entry** land here, and shelving lines the walls.
- Both baths are **en suite only**, with no hall bath.
- Ceilings are 10 ft in the bedrooms (suggested) and 9 ft in the halls.

**Garage (front right)**
- **Two-car** (his truck plus her SUV), as sketched, with **one insulated ~20'9" × 10' door** facing the street (x 80.4–101.2 at y 66.5).
- A **5 ft side roll-up door** on the right wall (x = 113, y 47.2–52.4) lets the riding mower out.
- Keep the **garage built-ins** as sketched: lockers, deep shelving, a storage closet and cabinets on the right side.
- **About 11'6" ceiling** for the 10 ft door. That pushes the bonus floor up about 2 steps.
- A **ductless mini-split** on the back wall and a **Level 2 EV charger** on the truck bay wall.
- The garage-to-hall door (x 87–90 at y 40) opens near the drop zone.
- **Standby generator pad** (3' × 5') outside, tight to the garage side wall in the notch below the roll-up, at (107.9, 58.4). Size it at 24–26 kW air-cooled with an automatic transfer switch.

**Upstairs bonus (open: one room or two)**
- Over the garage, x 78.5–107.5, y 40–66.5, reached by the stairs.
- **Option 1:** one 29' × 17' bonus room, plus a full bath, a closet and attic storage along the front.
- **Option 2:** two rooms off a back hall, each with a closet, sharing a bath. Either room can be an office or a bedroom.
- Usable width depends on the roof pitch and dormers.

### Ceiling plan

| Room | Height | Treatment | Status |
|---|---|---|---|
| Living room | 12' | Exposed sinker cypress beams ~4 ft on center, running to the front doors | **Decided** |
| Kitchen + dining | 11' | Flat plaster; the hood runs to the ceiling | **Decided** |
| Lounge | 11' | Shallow coffers | Suggested |
| Primary bedroom | 11' | Tray with indirect cove light | Suggested |
| Office, bedrooms 2 and 3 | 10' | Flat; acoustic plaster in the office | Suggested |
| Halls, baths, closets | 9' | Flat (lower, so the rooms off them feel taller) | Suggested |
| Garage | ~11'6" | For the 10 ft door | Decided |
| Front door / glass wall | ~10' tall openings | | Working assumption |

### Materials palette (from the interior design pass)
- **Reclaimed heart pine floors**, wide plank and oiled, in every room except the wet rooms.
- **Sinker cypress** for the living room beams, the media wall, the front doors and the powder vanity.
- **Limewash plaster walls** in the great room, entry and primary suite.
- **Honed white marble** for the island, the perimeter counters and the powder vanity.
- **Unlacquered brass** hardware and faucets.
- **Deep green lacquer** in the lounge library.
- **Limestone** for the lounge fireplace surround and the primary bath floor.
- **Handmade zellige** for the scullery backsplash and the primary shower.

Lighting:
- Layered lighting with few downlights: cove, sconces and picture lights, tunable white, on a Lutron-type system.
- Motorized shades recessed into ceiling pockets.
- Invisible plaster speakers.

### Systems and building specs (decided)
- **Conditioned spray-foam attic.** The HVAC and water heater go in the attic, so there's no mechanical room. Add a whole-house dehumidifier, and a drain pan with a leak sensor under the water heater.
- **Standby generator** (see the garage section). It also carries the pond pumps.
- **Low-voltage plan** (see `images/03` and the JSON), all home-run to the rack in the server room:
  - 16 PoE cameras around the eaves for Scrypted, plus a video doorbell.
  - 9 Wi-Fi access points, two of them outdoors.
  - Cat6 drops at every TV and desk.
  - Ceiling speakers in the living room, lounge, back porch and outdoor kitchen.
  - Conduit stubs to the outdoor kitchen, side porch, pond and gate.
- **Outdoor kitchen:** a U against the office wall. The bar with stools is the left leg, and the grill is on the back run.
- **Porch screens: open.** The options are motorized retractable screens on the back porch, fixed screens on the side porch, or none. Ceiling fans go on every porch either way.

---

## 5. Decided vs. rejected (don't reintroduce rejected items)

**Decided (yes):**
- A 16 ft glass wall on the front-door axis, keeping the porch door.
- A 12 ft beamed living room, and an 11 ft kitchen and dining.
- A plaster hood, a scullery, and dining French doors with a wine wall.
- The lounge as a library, with steel-and-glass doors and a flush gas fireplace on its left wall.
- A dressing room.
- Sound isolation for the office and the laundry.
- Powder room option A.
- Bedroom 3 option A.
- The garage as sketched (one wide door, side roll-up for the mower, built-ins kept), with a 10 ft insulated door, mini-split and EV charger.
- The generator pad by the garage side wall.
- A conditioned attic, and HVAC and water heater in the attic.
- The server room holds the panels and broadband.
- The range behind the island, the island at 6 ft with a 48 in aisle, and the sink between two dishwashers.
- The drop zone left of the garage door.
- The stair with one big under-stair closet.
- A linen closet in the bedroom passage.
- The office as drawn, with a couch, his computer desk and a big OLED TV on the porch-side wall.
- The round table in the dining room.
- A water feature (small pond) by the front porch.
- The long pond (rev. D) out back.

**Rejected (no):**
- A foyer or coat closet.
- A second office window.
- Turning the office into a theater room.
- A fireplace in the living room media wall.
- A primary wet room.
- A lowered entry ceiling band.
- Vessel sinks anywhere.
- A safe room.
- An outside (pool) door from bath 2.
- Flood-elevation changes.
- A mechanical room.
- A garage door from the scullery (it's a hatch only).
- A closet island in the dressing room.

**Standing rules from the owners:**
- Stay faithful to the hand sketch. Don't invent or drop built-ins.
- Cabinetry sits **flush on wall faces**, never in doorways or walkways.
- The lounge stays about 17 ft wide.

---

## 6. Landscape: the long recreation pond (rev. D, decided)

The back yard centers on an **Aquascape-style natural swimming pond** (in the style of Greg Wittstock and Aquascape). It has no chlorine: a planted wetland filters the water.

**Geometry.** All of it is in `data/pond-rev-d.json`, using the house's axes. The outline is control points, smoothed with a closed Catmull-Rom curve. z = 0 is the water level.
- The pond is about **2,395 sf** and **80 ft long**, running **across the back of the house** from about x 3 to x 85, between y +5 and y -39. It holds about **66,000 gal**.
- **Depths:** 0 to 18 in at the beach, a 12 in sun ledge, a **5 ft lap lane close to 70 ft long**, and an **8 ft deep zone** under the jump rock.
- **Wetland filter:** about **964 sf (40% of the pond)**. It's a two-tier crescent forming the **far (back) shore**:
  - The **upper tier** is about 3½ ft up and feeds a **7 ft wide waterfall with about a 3½ ft drop**, centered on **x = 37.5**, the main axis.
  - The **lower tier** is about 1 ft up and sheets water over **a 36 ft low stone lip**, then down a rill into a **lily cove** at the right end.
  - The land behind it rises on a long, low slope built from the pond's spoil.

**Near shore (by the house)**
- A **flagstone terrace** (about 1,000–1,200 sf) runs from the back porch and outdoor kitchen down to **cut-stone coping** at the water. There is no deck.
- A **12 in sun ledge** sits in front of the porch, with chaises standing in the water, and three **slab steps** lead into the lap lane.
- A **pea-gravel beach** is at the left end.
- An **intake bay (skim cove)** sits in the far-left corner. The **pump vault** is past the bedroom wing at (-7.6, -27.2), screened by shrubs.

**Far shore and around**
- A **flat jump rock** over the deep zone.
- A **fire pit circle** with six chairs across the water on the far-left shore, at (12.4, -46).
- A **stepping-stone loop** with an **overlook bench** on the back slope, at (42, -76.4), and a bench at the right end.
- A **pool barrier fence** (dashed on the plan), if the city requires one. The house's back wall closes it.

**The yard beyond the pond**
- **Cajun prairie meadow** behind the pond, with a native **tree line** of wax myrtle, Savannah holly, yaupon, southern magnolia and bald cypress.
- **Live oaks** shade the fire pit side and the lawn. Keep big trees at least 25 ft from the water.
- An **open lawn** (St. Augustine or zoysia) on the right, behind the office and primary suite.
- A **mower route** from the garage side roll-up, over a paver apron, up a gravel path.
- A **hedged primary garden** behind the primary bath, lined up on the tub window, with a basalt-column bubbler, a Japanese maple and a bench.
- A **cedar outdoor rinse shower** in the office/primary-bath corner.
- An optional **kitchen garden** of six raised beds by the garage side.
- A **shade garden** along the bedroom wing.

**Front yard**
- A small **ecosystem pond** (about 11' × 7') in the courtyard between the front porch and the scullery, visible from the porch and the kitchen sink window.
- A **curved flagstone walk** to the drive, low beds along the fronts, and shade and flowering trees.

**Equipment and engineering**
- External pumps for about one turnover an hour, Centipede modules under the wetland, IonGen G2 and auto dosing, and jets and aeration.
- A 45 mil EPDM liner.
- A **sub-liner drain, sump and vent** for the high water table.
- A raised rim and swale to keep runoff out, and an overflow sized for 10 in rain events.
- Pumps on the standby generator.
- The 5 ft zone stays outside a 45° line down from the porch footing.

**Plants:** zone 9a and Louisiana natives (Louisiana iris, pickerelweed, soft rush, water lilies, Gulf muhly, dwarf palmetto, and so on). The full palette is in `reference/landscape-plan.html`.

**Budget (rough, whole landscape):** $235k–$416k, with the pond itself at $130k–$210k.

---

## 7. Exterior: a placeholder style (yours to develop)

No exterior design exists yet. The working placeholder is **Acadian-modern**:
- **White board-and-batten** siding.
- A **dark standing-seam metal roof**.
- **Black windows**.
- **Cypress porch posts**.
- **Deep covered porches.**

Acadian cues worth considering:
- Steep side-gabled main roofs.
- Porches tucked under the main roofline or a lower shed roof.
- Raised floors with a few steps up.
- Tall, vertically proportioned windows.

The stills in `images/3d-placeholder/` show one quick take on this placeholder (side-gabled dark metal roofs, gabled dormers over the garage, shed-roof porches). Treat them as a massing check only. You're free to do better.

Roof form, pitch, massing, the bonus-floor dormers and whether the garage roof reads as a separate wing are all **yours to propose**. Keep these constraints:
- The bonus room over the garage needs a roof that gives usable headroom.
- The ~11'6" garage ceiling sits under the bonus floor.
- The **16 ft glass wall** and the front doors stay legible as **one axis** from the front walk through to the pond.
- The house should feel calm and rooted in south Louisiana, not themed.

---

## 8. Open questions (propose answers, labeled as proposals)

1. **Upstairs:** one bonus room or two rooms?
2. **North orientation:** unknown. It affects porch sun, shade trees and the side of the fire pit.
3. **Porch screens:** motorized on the back porch, fixed on the side porch, or none?
4. **Suggested ceilings** (lounge, primary, office, bedrooms, halls) are not yet confirmed.
5. **Fish in the pond:** koi, native fish (bluegill, mosquitofish) or both? Some fish are close to a must for mosquitoes.
6. **Pool barrier:** whether Youngsville treats the pond as a pool. If so, a 4 ft barrier, plus alarms or self-closing hardware on the glass wall, porch door and dining doors.
7. **FEMA zone** for the pond area.
8. **The bedroom wing and stairs** may be redrawn by Michael's wife.
9. **Cabinet elevations** haven't been drawn.
10. **Structural engineer** for the 16 ft glass-wall header and the moved porch post, and an early quote for the glass wall.

---

## 9. What to produce

Michael wants to see how a different designer interprets this. Please produce as much of the following as you can, and say which items you skipped.

1. **Main-floor plan, dimensioned**, faithful to the coordinates above. Show walls, doors with swings, windows, the glass wall, built-ins and room names with sizes.
2. **Furnished plan**, matching the furniture described here (use `images/01` as the reference).
3. **Upstairs plan(s)**: both options, or your recommended one.
4. **Reflected ceiling plan** with the heights and treatments above.
5. **Four exterior elevations** (front, back, left, right) in the Acadian-modern style, plus a **roof plan**.
6. **Building section on the main axis** (x = 37.5): front porch, front doors, beamed living room, glass wall, back porch, terrace, sun ledge, pond and falls.
7. **3D model** of the house and site, with the pond, terrace and key landscape. Export it to a common format (glTF/GLB preferred, or OBJ/FBX), or as an interactive web viewer.
8. **Renders:**
   - **Exterior:** the front from the drive (day), the back from across the pond at dusk with the falls lit, and an aerial three-quarter view of the whole site.
   - **Interior:** the living room from the front doors looking through the glass wall to the pond, the kitchen with the hood and island, the lounge library with the fireplace, and the primary bath.
9. **Site/landscape plan** at your own drafting quality, consistent with `data/pond-rev-d.json`.
10. **A short notes page** listing any assumptions you made, any conflicts you found in this brief, and anything you'd change and why. Keep your suggestions separate from the brief.

**Please don't** reintroduce anything in the rejected list, move the main axis, or change decided room sizes without flagging it.

---

*This is a planning-level design, not construction documents. Walls are within about ±1 ft of the original hand sketch. Brands named are examples of a type, not a specification.*
