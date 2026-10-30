import subprocess, json, re, os

pages = [
    'index.html',
    'projecten.html',
    'project-your-bubble-in-the-noise.html',
    'project-smeltende-sieraden.html',
    'project-whiplash-optiteling.html',
    'project-stop.html'
]
widths = [390, 768, 1440]
chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

script_js = '''
window.addEventListener('load', async () => {
    // wait for all images to load
    const imgs = Array.from(document.querySelectorAll('img'));
    await Promise.all(imgs.map(img => {
        if (img.complete && img.naturalWidth > 0) return Promise.resolve();
        return new Promise(r => {
            img.onload = r;
            img.onerror = r;
            // timeout fallback 1.5s
            setTimeout(r, 1500);
        });
    }));

    const results = [];
    imgs.forEach((img, idx) => {
        const rect = img.getBoundingClientRect();
        const style = window.getComputedStyle(img);
        const parent = img.parentElement;
        const parentRect = parent ? parent.getBoundingClientRect() : null;
        results.push({
            idx: idx,
            src: img.getAttribute('src'),
            alt: img.getAttribute('alt') || '',
            naturalWidth: img.naturalWidth,
            naturalHeight: img.naturalHeight,
            renderedWidth: Math.round(rect.width),
            renderedHeight: Math.round(rect.height),
            parentClass: parent ? parent.className : '',
            parentWidth: parentRect ? Math.round(parentRect.width) : 0,
            parentHeight: parentRect ? Math.round(parentRect.height) : 0,
            objectFit: style.objectFit,
            aspectRatio: style.aspectRatio
        });
    });
    console.log('AUDIT_DATA:' + JSON.stringify(results));
});
'''

for page in pages:
    with open(page) as f:
        html = f.read()
    # remove loading="lazy" in audit copy so they load immediately
    html_mod = html.replace('loading="lazy"', 'loading="eager"')
    injected_html = html_mod.replace('</body>', f'<base href="http://localhost:8085/"><script>{script_js}</script></body>')
    with open(f'scratch/audit_{page}', 'w') as f:
        f.write(injected_html)

all_data = {}

for page in pages:
    all_data[page] = {}
    tmp_url = f'http://localhost:8085/scratch/audit_{page}'
    for w in widths:
        cmd = [
            chrome,
            '--headless',
            '--disable-gpu',
            '--screenshot=scratch/tmp.png',
            f'--window-size={w},2500',
            '--virtual-time-budget=4000',
            '--enable-logging=stderr',
            tmp_url
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        stderr_txt = proc.stderr.decode('utf-8', errors='ignore')
        
        match = re.search(r'AUDIT_DATA:(\[.*?\])(?=",\s*source:|\n|$)', stderr_txt)
        if match:
            try:
                data = json.loads(match.group(1))
                all_data[page][w] = data
            except Exception:
                try:
                    raw = match.group(1).encode('utf-8').decode('unicode_escape')
                    all_data[page][w] = json.loads(raw)
                except Exception as e:
                    all_data[page][w] = f'JSON err: {e}'
        else:
            all_data[page][w] = 'No match'

with open('scratch/audit_metrics.json', 'w') as f:
    json.dump(all_data, f, indent=2)

print('Audit metrics collected with image loads!')
