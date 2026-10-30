import os
import subprocess

pages = [
    ("index_full", "http://localhost:8085/index.html", 1440, 3200),
    ("projecten_full", "http://localhost:8085/projecten.html", 1440, 4200),
    ("your-bubble_full", "http://localhost:8085/project-your-bubble-in-the-noise.html", 1440, 5200),
    ("smeltende-sieraden_full", "http://localhost:8085/project-smeltende-sieraden.html", 1440, 4800),
    ("stop_full", "http://localhost:8085/project-stop.html", 1440, 6000),
    ("whiplash_full", "http://localhost:8085/project-whiplash-optiteling.html", 1440, 4600),
]

out_dir = "/Users/fee/Desktop/CMD/Jaar 2/Periode 5/Collectief 5/portfolio map/portfolio 6/scratch/verification_screenshots"
chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for p_name, url, w, h in pages:
    out_file = os.path.join(out_dir, f"{p_name}.png")
    cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={w},{h}",
        f"--screenshot={out_file}",
        url
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Captured {p_name} -> {out_file}")

print("Full-height screenshots captured.")
