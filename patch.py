content = open('index.html').read()

# 1. Make exportFortune async
content = content.replace('function exportFortune() {', 'async function exportFortune() {')

# 2. Replace cookie drawing call
content = content.replace(
    '      // Draw fortune cookie\n      drawCanvasCookie(ctx, size/2, size * 0.24, size * 0.11);',
    '      // Draw cookie emoji reliably\n      await drawEmoji(ctx, \'🥠\', size/2, size * 0.25, size * 0.17);'
)

# 3. Replace the whole drawCanvasCookie function with drawEmoji
old_fn_start = '    function drawCanvasCookie(ctx, cx, cy, r) {'
old_fn_end = '    }'
# find and replace entire drawCanvasCookie function
import re
content = re.sub(
    r'    function drawCanvasCookie\(ctx, cx, cy, r\) \{.*?\n    \}',
    '''    function drawEmoji(ctx, emoji, cx, cy, size) {
      return new Promise(resolve => {
        const off = document.createElement('canvas');
        off.width = size * 2; off.height = size * 2;
        const octx = off.getContext('2d');
        octx.font = `${size * 1.6}px serif`;
        octx.textAlign = 'center';
        octx.textBaseline = 'middle';
        octx.fillText(emoji, size, size);
        // Give browser a frame to render the emoji
        requestAnimationFrame(() => {
          ctx.drawImage(off, cx - size, cy - size, size * 2, size * 2);
          resolve();
        });
      });
    }''',
    content,
    flags=re.DOTALL
)

open('index.html', 'w').write(content)
print("Done")
