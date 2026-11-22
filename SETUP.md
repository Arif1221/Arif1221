# GitHub profile setup

This package is designed for the special profile repository `Arif1221/Arif1221`.

## Included files

```text
.
├── README.md
├── SETUP.md
├── assets/
│   └── listening-card.gif
└── .github/
    └── workflows/
        └── snake.yml
```

## Install

1. Extract this ZIP.
2. Copy `README.md`, `assets/`, and `.github/` into the root of `Arif1221/Arif1221`.
3. Keep the folder paths exactly as shown. In particular, `.github` must be at the repository root.
4. Commit the changes to the `main` branch.
5. Open **Actions → Update contribution animation** and run it once with **Run workflow** if the latest snake image has not yet been generated.

The workflow runs automatically once a day after the first successful run.

## Verify the contribution animation

The workflow publishes two files to the `output` branch:

- `github-contribution-grid-snake.svg`
- `github-contribution-grid-snake-dark.svg`

The README points to those exact filenames. The output branch is separate from `main`; do not copy the generated SVGs into `main` manually.

If the workflow cannot push to `output`, open **Repository Settings → Actions → General → Workflow permissions** and enable **Read and write permissions**. The workflow uses GitHub's built-in `GITHUB_TOKEN`; no personal access token or external secret is required.

## Dynamic services

The README uses external image services for the typing animation, GitHub statistics, language distribution, profile-view counter, follower badge and technology icons. They update independently and may occasionally be delayed or rate-limited by their providers.

The music card is a locally stored animated GIF. It links to the Spotify track, but it does not report live Spotify playback status.

## Customization

- Change the typing lines in the `readme-typing-svg.demolab.com` URL in `README.md`.
- Add or remove technology icons in the `skillicons.dev` URLs.
- Update project descriptions as their implementation status changes.
- Replace `assets/listening-card.gif` to feature a different track or visual.
