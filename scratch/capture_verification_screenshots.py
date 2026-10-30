import os
import subprocess
import time

pages = [
    ("index", "http://localhost:8085/index.html"),
    ("projecten", "http://localhost:8085/projecten.html"),
    ("your-bubble", "http://localhost:8085/project-your-bubble-in-the-noise.html"),
    ("smeltende-sieraden", "http://localhost:8085/project-smeltende-sieraden.html"),
    ("stop", "http://localhost:8085/project-stop.html"),
    ("whiplash", "http://localhost:8085/project-whiplash-optiteling.html"),
]

widths = [390, 768, 1440, 1920]
height = 1080

out_dir = "/Users/fee/Desktop/CMD/Jaar 2/Periode 5/Collectief 5/portfolio map/portfolio 6/scratch/verification_screenshots"
os.makedirs(out_dir, exist_ok=True)

chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for p_name, url in pages:
    for w in widths:
        out_file = os.path.join(out_dir, f"{p_name}_{w}px.png")
        cmd = [
            chrome_bin,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={w},{height}",
            f"--screenshot={out_file}",
            url
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Captured {p_name} at {w}px -> {out_file} (returncode: {res.returncode})")

print("All verification screenshots taken.")
