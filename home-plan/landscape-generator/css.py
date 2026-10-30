CSS = r'''
.ls text{text-anchor:middle;font-family:var(--f-body)}
.road{fill:#B4B0A7}.curb{stroke:#8E897F;stroke-width:.3}
.mow{stroke:#C4D69A;stroke-width:3.2;stroke-linecap:round}
.berm{fill:#B9CC8E;stroke:#8DA866;stroke-width:.12}
.sh{fill:#86A962;stroke:#5B7B3F;stroke-width:.1}.sh2{fill:#9DB98A;stroke:#68845A;stroke-width:.1}
.sh3{fill:#B98FA6;stroke:#7E5A6E;stroke-width:.1}.fern{fill:#6F9A5A;stroke:#4C703C;stroke-width:.1}
.hedge{fill:#5E8A4E;stroke:#41663A;stroke-width:.1}.veg{fill:#8DB55F;stroke:#5E853B;stroke-width:.08}
.grout{fill:#B8AC97}.fg1{fill:#DDD3C2;stroke:#A99D88;stroke-width:.06}.fg2{fill:#D3C8B4;stroke:#A99D88;stroke-width:.06}.fg3{fill:#E5DCCD;stroke:#A99D88;stroke-width:.06}
.deck{fill:#C79E6B;stroke:#87653E;stroke-width:.12}.board{stroke:#A07C51;stroke-width:.06}
.fence{fill:none;stroke:#87653E;stroke-width:.3}.fenceg{fill:none;stroke:#87653E;stroke-width:.22;stroke-dasharray:.6 .3}
.axisl{stroke:#B0812A;stroke-width:.32;stroke-dasharray:1.2 .8;opacity:.75}.bfence{fill:none;stroke:#7A5A36;stroke-width:.32;stroke-dasharray:1.1 .5}
.dg{fill:#E4D8BF}.edge{fill:none;stroke:#8E8270;stroke-width:.18}
.st{fill:#B8B0A3;stroke:#6E665A;stroke-width:.1}.st2{fill:#A9A195;stroke:#655D52;stroke-width:.1}.st3{fill:#C4BDB1;stroke:#7A7266;stroke-width:.1}
.sth{fill:#fff;opacity:.22}.shd{fill:#2E2C27;opacity:.2}
.slab{fill:#CFC6B6;stroke:#7A7266;stroke-width:.12}
.pit{fill:#4A443D}.fire{fill:#E58B3A}
.bench{fill:none;stroke:#9C9384;stroke-width:1;stroke-linecap:round}
.w1{fill:#9FCFDF}.w2{fill:#6FAAC2}.tint{fill:#8CC4D8;opacity:.55}
.tier{fill:#CBBE9E;opacity:.5;stroke:#8E7F62;stroke-width:.2}.wlb{stroke:#9E927A;stroke-width:.12}
.rip{fill:none;stroke:#fff;stroke-width:.14;opacity:.55;stroke-linecap:round}
.foam{fill:none;stroke:#fff;stroke-width:.32;stroke-linecap:round;opacity:.9}.foam2{fill:none;stroke:#fff;stroke-width:.3;stroke-linecap:round;opacity:.85}
.foamb{fill:#F3FAFC;opacity:.85}
.tf{fill:none;stroke:#557A3C;stroke-width:.13;stroke-linecap:round}.tf2{fill:none;stroke:#7C9E4C;stroke-width:.13;stroke-linecap:round}
.pk{fill:#6F9850}.pkf{fill:#8C6CC0}.ir{fill:#7FA6A0;stroke:#567A72;stroke-width:.08}
.lp{fill:#6E9B4F;stroke:#4C7536;stroke-width:.08}.lf{fill:#F4C3D2}.lf2{fill:#FFF8E8}
.ladder{fill:none;stroke:#7B8088;stroke-width:.18}
.umb{fill:#F2EDE2;stroke:#B4A88F;stroke-width:.1;opacity:.92}
.pot{fill:#C9A37E;stroke:#8A6A48;stroke-width:.1}
.vault{fill:#7E7A72;stroke:#55524C;stroke-width:.1}
.tshd{fill:#2E3A24;opacity:.16}
.t-dec{fill:#7EA457;stroke:#557A38;stroke-width:.14;opacity:.93}.t-dec-hi{fill:#A3C47A;opacity:.45}
.t-maple{fill:#A8513D;stroke:#76321F;stroke-width:.14;opacity:.93}.t-maple-hi{fill:#C9765E;opacity:.5}
.t-birch{fill:#A9C77A;stroke:#78944F;stroke-width:.14;opacity:.9}.t-birch-hi{fill:#CDE0A6;opacity:.5}
.t-ever{fill:#46704A;stroke:#2F5133;stroke-width:.14}.t-ever-hi{fill:#5F8A5E;opacity:.55}
.t-orn{fill:#C98BB0;stroke:#8C5878;stroke-width:.12;opacity:.93}.t-orn-hi{fill:#E2B3CE;opacity:.55}
.tbr{stroke:#4D3F2E;stroke-width:.1;opacity:.35}.ttr{fill:#5A4632}
.bed{fill:#C6B48F;stroke:#9C8A66;stroke-width:.1}
.basalt{fill:#4F5257;stroke:#2F3135;stroke-width:.08}
.gpath{fill:#E1D7C2;stroke:#B8AC92;stroke-width:.1}.pav{fill:#CFC5B3;stroke:#A1957F;stroke-width:.1}
.rbed{fill:#9B7B57;stroke:#6E5436;stroke-width:.12}
.drive{fill:#D6D0C3;stroke:#ABA394;stroke-width:.12}
.lot{fill:none;stroke:#6E6556;stroke-width:.22;stroke-dasharray:1.4 .7}
.lg{fill:#FFE08A;opacity:.85}.lgc{fill:#FFF6D5;stroke:#C9A23B;stroke-width:.06}
.plan.ls text.lt{font-size:2.1px;font-weight:600;fill:#23272E;paint-order:stroke;stroke:#FBF8F1;stroke-width:.5px;stroke-linejoin:round}
.plan.ls text.lt2{font-size:1.5px;font-style:italic;fill:#3F4650;paint-order:stroke;stroke:#FBF8F1;stroke-width:.4px;stroke-linejoin:round}
.plan.ls.zoom text.lt{font-size:1.45px}.plan.ls.zoom text.lt2{font-size:1.05px}
.plan.ls text.dep{font-size:1.2px;font-weight:600;fill:#fff;opacity:.95}
.co circle{fill:#8A6A2F;stroke:#FBF8F1;stroke-width:.18}.plan.ls .co text{font-size:1.15px;font-weight:700;fill:#fff}
.plan.ls .cap text{font-size:1.6px;fill:#6E6556;text-anchor:start;letter-spacing:.08px}
.scale rect{fill:#3A3F48}.scale rect.o{fill:#FBF8F1;stroke:#3A3F48;stroke-width:.12}.plan.ls .scale text{font-size:1.3px;fill:#3A3F48;text-anchor:start}
.sec text{font-family:var(--f-body)}
.d-key{columns:2;column-gap:28px;margin:14px 0 0;padding-left:1.6em}.d-key li{margin:.3em 0;break-inside:avoid}
@media (max-width:640px){.d-key{columns:1}}
.flow{display:block;width:100%;height:auto}
'''
CSS += r'''
.plan.sec text.sn{font-size:1.25px;fill:#3A3F48;paint-order:stroke;stroke:#FBF8F1;stroke-width:.35px;stroke-linejoin:round}.plan.sec text.sd{font-size:1.2px;fill:#3A3F48;font-weight:600;paint-order:stroke;stroke:#FBF8F1;stroke-width:.3px}
.flow{color:var(--ink,#1B2533);margin:6px 0}
'''
