# GitHub Deployment & Update Guide (Step-by-Step)

Follow these steps to update your GitHub repository:

### Method 1: Using GitHub Web Interface (Simplest, Zero Tools)
1. Go to your GitHub repository in your web browser (e.g. `https://github.com/your-username/dbyc-portal`).
2. Click the **Add file** button (top right) -> choose **Upload files**.
3. Drag and drop all the files from this folder (`GITHUB_UPDATE_FILES`):
   - `index.html`
   - `sw.js`
   - `manifest.json`
   - `.nojekyll`
   - `README.md`
   - The entire `assets/` folder (`logo.png`, `icon.png`, `icon.jpg`)
4. At the bottom under "Commit changes", type:
   `Update DBYC portal with 12 master corrections and PIN login`
5. Click the green **Commit changes** button.
6. Done! GitHub Pages will automatically update within 60 seconds.

### Method 2: Using Git CLI / Terminal
If you use Git on your computer, run these commands in your repository folder:
```bash
git add .
git commit -m "Update DBYC portal: 12 master corrections, PIN login, A4 printing, Google Lens attendance"
git push origin main
```
