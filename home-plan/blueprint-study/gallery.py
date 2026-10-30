import sys; sys.path.insert(0, '/tmp/claude-0/work/study'); import page
OUT = '/tmp/claude-0/-home-user/e6115272-0448-5bf5-821a-8a9256a6084c/scratchpad/gallery/index.html'
def g(items):
    return '<div class="gal">' + ''.join(f'<figure><button class="th" type="button" aria-label="Open {c} full screen"><img src="img/{f}" alt="{c}" loading="lazy"></button><figcaption>{c}{(" <span class=\'chip " + k + "\'>" + t + "</span>") if t else ""}</figcaption></figure>' for f, c, k, t in items) + '</div>'
M = ['''<header class="d-head"><div class="d-top"><span class="d-type">Design options</span><span class="d-date">Draft L → M · Oct 29, 2026</span></div>
<h1 class="d-title">Floor plan option drawings</h1>
<p class="d-lead">Every labeled plan from today's blueprint work in one place. Tap an image to open it full size, then press and hold to save or share it.</p></header>''',
'<h2 class="d-h2">Suite foyer space (draft M)</h2><p class="d-note">Ideas for the 10 × 7 space between the primary bedroom and the hall. The first three are open to the hall, not walled in (Oct 30). Waiting on your pick.</p>', g([
 ('suite-foyer-7.png', "7 \u00b7 Open coffee and wine bar alcove", "neu", "Open"),
 ('suite-foyer-8.png', "8 \u00b7 Open library nook with a hidden bookcase door", "ok", "Recommended open"),
 ('suite-foyer-9.png', "9 \u00b7 Open household desk and charging niche", "neu", "Open"),
 ('suite-foyer-1.png', "1 \u00b7 Back-door suite with a his walk-in behind the bed", "ok", "Rec. walled"),
 ('suite-foyer-2.png', "2 \u00b7 Walk-through dressing room (smallest change)", "neu", "Smallest change"),
 ('suite-foyer-3.png', "3 \u00b7 Morning room: makeup vanity and coffee bar", "neu", ""),
 ('suite-foyer-4.png', "4 \u00b7 Powder west, hall closet, open east entry", "neu", ""),
 ('suite-foyer-5.png', "5 \u00b7 Wine room off the dining room (bold)", "neu", ""),
 ('suite-foyer-6.png', "6 \u00b7 Guest bath with a vanity room, two-door suite entry", "neu", "")]),
'<h2 class="d-h2">Living room and kitchen</h2><p class="d-note">Waiting on your pick. I recommend G2.</p>', g([
 ('great-room-today.png', 'Today (draft L)', '', ''), ('great-room-g1.png', 'G1 · Plan reset', 'neu', 'Budget'),
 ('great-room-g2.png', 'G2 · Cathedral living room', 'ok', 'Recommended'), ('great-room-g3.png', 'G3 · Plus a pond dormer', 'neu', 'Later'),
 ('great-room-section.png', 'Section: today vs G2', '', '')]),
'<h2 class="d-h2">Guest wing (bedrooms 2 and 3)</h2><p class="d-note">Waiting on your pick. I recommend wing G1: same footprint, no roof change.</p>', g([
 ('guest-wing-today.png', 'Today (draft L)', '', ''), ('guest-wing-g1.png', 'Wing G1 · Guest foyer', 'ok', 'Recommended'),
 ('guest-wing-w4.png', 'Wing W4 · West wall out 4 ft', 'neu', 'Upgrade'), ('guest-wing-v1.png', 'Wing V1 · Hotel suite plus flex', 'neu', 'Alternative')]),
'<h2 class="d-h2">Primary bedroom on the pond</h2><p class="d-note">You picked idea 1 and office layout 3.</p>', g([
 ('primary-on-pond-1-office-swap-v2.png', 'Idea 1 with the new office', 'ok', 'Picked'), ('primary-on-pond-office-3.png', 'Office layout 3 · Two rooms in one', 'ok', 'Picked'),
 ('primary-on-pond-office-1.png', 'Office layout 1', 'neu', 'Not chosen'), ('primary-on-pond-office-2.png', 'Office layout 2', 'neu', 'Not chosen'),
 ('primary-on-pond-today.png', 'Today (draft L)', '', ''), ('primary-on-pond-1-office-swap.png', 'Idea 1 (first version)', '', ''),
 ('primary-on-pond-2-pavilion.png', 'Idea 2 · Glass pavilion', 'neu', 'Not chosen'), ('primary-on-pond-3-bedroom-first.png', 'Idea 3 · Bedroom-first suite', 'neu', 'Not chosen'),
 ('primary-on-pond-4-falls-view.png', 'Idea 4 · Falls view', 'neu', 'Not chosen')]),
'<h2 class="d-h2">Earlier primary bath and closet options</h2><p class="d-note">These came before the move to the office spot. Option B (pushing the bath back) can still be added on top of idea 1 if Melissa wants a bigger closet and bath.</p>', g([
 ('primary-suite-draft-l.png', 'Draft L suite', '', ''), ('primary-suite-option-a.png', 'Option A', '', ''), ('primary-suite-option-b.png', 'Option B', '', ''), ('primary-suite-option-c.png', 'Option C', '', '')]),
'<footer class="d-foot">Drawn to scale from draft L. Sources: /mnt/project-files/home-plan/blueprint-study/.</footer>']
CSS = '''.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin:12px 0 28px}
.gal figure{margin:0;display:grid;gap:6px}.gal img{width:100%;height:auto;display:block;border:1px solid var(--rule);border-radius:4px;background:var(--surface)}
.gal figcaption{font-size:14px;color:var(--ink);display:flex;gap:8px;align-items:center;flex-wrap:wrap}'''
JS = '''<div id="lb" hidden role="dialog" aria-modal="true" aria-label="Drawing viewer">
<div class="lb-bar"><span id="lbcap"></span><span class="lb-btns"><button type="button" id="lbz">Zoom in</button><button type="button" id="lbp" aria-label="Previous">‹</button><button type="button" id="lbn" aria-label="Next">›</button><button type="button" id="lbx" aria-label="Close">✕</button></span></div>
<div class="lb-stage" id="lbs"><img id="lbi" alt=""></div></div>
<script>
(()=>{const th=[...document.querySelectorAll('.th')],lb=document.getElementById('lb'),im=document.getElementById('lbi'),st=document.getElementById('lbs'),cap=document.getElementById('lbcap'),z=document.getElementById('lbz');let i=0;
const show=k=>{i=(k+th.length)%th.length;const t=th[i].querySelector('img');im.src=t.src;im.alt=t.alt;cap.textContent=t.alt;lb.classList.remove('zoom');z.textContent='Zoom in';st.scrollTo(0,0);};
th.forEach((b,k)=>b.addEventListener('click',()=>{show(k);lb.hidden=false;document.body.style.overflow='hidden';}));
const close=()=>{lb.hidden=true;document.body.style.overflow='';};
const zoom=()=>{lb.classList.toggle('zoom');z.textContent=lb.classList.contains('zoom')?'Fit to screen':'Zoom in';};
document.getElementById('lbx').onclick=close;document.getElementById('lbp').onclick=()=>show(i-1);document.getElementById('lbn').onclick=()=>show(i+1);z.onclick=zoom;im.onclick=zoom;
addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1);});})();
</script>'''
CSS += '''
.th{all:unset;cursor:zoom-in;display:block}.th:focus-visible img{outline:2px solid var(--accent);outline-offset:2px}
#lb{position:fixed;inset:0;z-index:50;background:var(--bg);display:flex;flex-direction:column}
#lb[hidden]{display:none}
.lb-bar{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px max(16px,env(safe-area-inset-left,0px));border-bottom:1px solid var(--rule);color:var(--ink);font-weight:600}
.lb-btns{display:flex;gap:8px}.lb-btns button{font:600 15px "Source Sans 3",system-ui,sans-serif;min-width:44px;min-height:40px;padding:0 12px;border:1px solid var(--rule-strong);border-radius:6px;background:var(--surface);color:var(--ink);cursor:pointer}
.lb-stage{flex:1;overflow:auto;display:flex;align-items:flex-start;justify-content:center;padding:12px;-webkit-overflow-scrolling:touch;touch-action:pan-x pan-y pinch-zoom}
.lb-stage img{max-width:100%;max-height:100%;object-fit:contain;cursor:zoom-in;background:#fff}
#lb.zoom .lb-stage{justify-content:flex-start}#lb.zoom .lb-stage img{max-width:none;max-height:none;width:2200px;cursor:zoom-out}'''
open(OUT, 'w').write(page.wrap('Floor Plan Options', '\n'.join(M).replace('Tap an image to open it full size, then press and hold to save or share it.', 'Tap a drawing to view it full screen. Tap it again (or Zoom in) for full detail, and press and hold to save or share it.') + JS, CSS)); print('ok')
