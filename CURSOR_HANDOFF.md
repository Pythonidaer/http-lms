# HTTP LMS maintainer handoff

Read README.md and source-manifest.json first. `scripts/curriculum.py` authors the focused course. `scripts/build-course.py` generates course.json, index.html, course-stats.json and source-manifest.json from the curriculum and pinned MDN Markdown. Edit those inputs, then rebuild rather than editing the embedded JSON by hand.

The runtime preserves `optional` on reference decks and `collapsed` on outline sections. Optional references do not block sequential/final progression. Search filters title and slide text, temporarily expands matching sections and restores saved collapse preferences when cleared. Keep these behaviors in future refactors.

Run `node scripts/test-content.cjs` after changes and the Playwright browser suite for interaction/runtime changes. The local practice server is loopback-only and synthetic; do not promote it into a production API. Static hosted versions have no fixture endpoints.

The course intentionally keeps full API design and JSON grammar in separate LMS repositories. Preserve upstream attribution, notices and source pins when extending coverage. Client-side quiz results are learning feedback, not secure grades.
