cd /tmp/claude-0/-home-claude/a0365b26-e317-5a40-a062-30aeb8882135/scratchpad/three
for q in "out:front:16.75 front-afternoon" "out:front:16.75&siding=sage front-sage" "out:front:19.2 front-dusk" "out:corner:16 front-corner" "out:back:16.5 back-pond" "out:falls:17.25 from-fire-pit" "out:falls:16&cam=37.5,4,-28,37.5,0,-42,60 falls" "out:aerial:15 aerial"; do set -- $q; node shot.js "?still=$1" st3/$2.png 1920 1080 2>&1 | grep -v "GPU stall" | head -2; echo done $2; done
echo ALLDONE
