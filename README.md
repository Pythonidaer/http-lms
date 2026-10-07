# HTTP Learning Studio

A standalone HTTP LMS using the existing Learning Studio interface. Keep API and JSON as separate courses: this course teaches HTTP contracts and only the body-format/JavaScript knowledge needed to use them.

- 32 guided slide lessons (194 slides), with goals, exercises and worked checks.
- Eight module quizzes (25 questions) and an independent 18-question final; 80% passing, retakes enabled.
- Searchable optional reference: all **377 English MDN Web/HTTP pages** at pinned commit `bf7ff749b987d530e9a6c07f23ac66f94d968e57`, plus six supporting browser/JavaScript pages. 383 reference decks, 3,325 reference slides.
- Personal browser progress, notes, time tracking, learner reports/CSV and entire-course text copying.
- Responsive outline, mobile menu, keyboard controls and reduced-motion support.

The reference collection starts collapsed and never blocks core progression. All lessons are unlocked by default; settings can enable progression rules. Exercises are self-assessed. Quiz answers ship with the static site, so reports are study feedback rather than secure examination results.

## Sources and scope

The core path maps all eleven technical top-level topics in [freeCodeCamp’s HTTP Networking in JavaScript handbook](https://www.freecodecamp.org/news/http-full-course/) to original explanations and exercises grounded in [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP). The handbook is linked and mapped, not republished. See `source-manifest.json` for exact topic mappings, source URLs, notices, file checksums and lesson IDs.

MDN reference slides include its guide, header, method, status, CSP and Permissions Policy text. This is a dated snapshot, including experimental, deprecated and non-standard content with source flags. Generated compatibility/specification widgets link to live MDN; diagrams link to original assets with descriptions. Linked IETF specifications and external manuals are not reproduced. Raw upstream Markdown is retained under `docs/mdn/`; source macros and HTML tables are adapted for the slide reader. Examples remain inert text. No analytics, external scripts, browser dependency or backend is required for reading.

MDN text adaptations are distributed under [CC BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/), with attribution on every reference and the manifest. Upstream code licensing and the complete MDN license notice are in [docs/mdn/LICENSE.md](docs/mdn/LICENSE.md). The original guided text is also CC BY-SA 2.5. Vendored Marked retains its MIT license under `vendor/`.

## Run and practice

```sh
node scripts/practice-server.cjs
```

Open **http://localhost:8000**. Stop with Ctrl+C. The dependency-free server binds only to loopback and serves both the course and synthetic practice endpoints; writes are not persisted.

| Endpoint | Behavior |
|---|---|
| `GET /lessons` | 200 JSON |
| `HEAD /lessons` | Headers without content |
| `POST /lessons` | JSON with nonempty title → 201 and Location; 400/413/415/422 validation outcomes |
| `/missing` | 404 JSON |
| `/empty` | Bodyless 204 |
| `/invalid-json` | 200 with malformed JSON |
| `/redirect` | 303 to `/lessons` |
| `/etag` | 200 with ETag; matching If-None-Match → bodyless 304 |
| `/slow` | Delayed response for abort practice |

For a static host, publish the repository root (for example GitHub Pages). The reader works independently of the practice server; its synthetic endpoints are available only locally.

## Rebuild and verify

Authoring requires Python, `beautifulsoup4` and `markdownify`; the website itself needs none of these. The download checks each file against its upstream Git blob SHA.

```sh
python3 -m pip install beautifulsoup4 markdownify
python3 scripts/fetch-sources.py
python3 scripts/build-course.py
node scripts/test-content.cjs
```

Keep `course.json` and its embedded copy in `index.html` synchronized by rebuilding. To update sources, deliberately update the inventory and pinned commit together; the scripts do not silently fetch latest content.

Browser regression checks require Playwright and its Chromium installation:

```sh
npm install --no-save playwright
npx playwright install chromium
node scripts/test-browser.cjs
```

Tests verify source checksums/coverage, runtime validation, embedded parity, slide limits/fences, practice outcomes, responsive widths, mobile menu, search/collapse, optional reference progression, final scoring/reporting and unsafe source HTML. Optional test environment variables: `CHROMIUM_PATH`, `CHROMIUM_ARGS_MODULE`, `LMS_TEST_ARTIFACTS`.
