"""Original guided lessons; technical authority and deeper examples are MDN."""
MDN='https://developer.mozilla.org/en-US/docs/'
HANDBOOK='https://www.freecodecamp.org/news/http-full-course/'
HANDBOOK_MAP=[
 {'topic':'Why HTTP?','lessons':['exchange','roles']},
 {'topic':"JavaScript's Fetch API",'lessons':['fetch-basics','inspect-network']},
 {'topic':'What is DNS?','lessons':['dns']},
 {'topic':'What are URIs?','lessons':['url-parts','query-path']},
 {'topic':'Async/Await','lessons':['async-flow']},
 {'topic':'Error Handling','lessons':['fetch-errors']},
 {'topic':'HTTP Headers','lessons':['header-basics','inspect-network']},
 {'topic':'What is JSON?','lessons':['body-formats']},
 {'topic':'HTTP Methods','lessons':['method-contracts','write-methods','status-families']},
 {'topic':'URL Paths and Parameters','lessons':['query-path','resource-contracts']},
 {'topic':'What is HTTPs?','lessons':['https']},
]

def deck(id,title,objective,pairs,practice,check,refs):
    source='\n\n'.join(f'[{label}]({MDN+slug})' for label,slug in refs)
    slides=[('Goal and sources',objective+'\n\n'+source)]+pairs+[('Practice — try it first',practice),('Worked self-check',check)]
    return dict(id=id,type='slides',title=title,slides=[dict(id=f'{id}-s{i+1}',title=t,body=b) for i,(t,b) in enumerate(slides)])

def module(id,title,decks,skill=None,qs=None):
    if qs:decks.append(dict(id=id+'-check',type='quiz',title='Skill check: '+skill,skill=skill,questions=[dict(id=f'{id}-q{i+1}',prompt=p,options=o,answer=a,explanation=e) for i,(p,o,a,e) in enumerate(qs)]))
    return dict(id=id,type='section',title=title,children=decks)

def D(id,title,obj,pairs,practice,check,paths):
    return deck(id,title,obj,pairs,practice,check,[(p.split('/')[-1].replace('_',' '),p) for p in paths])

def make_course():
    start=D('start','Start here','Learn HTTP without turning the API and JSON courses into prerequisites.',[
      ('A short learning path plus a reference shelf','Work through the guided modules one lesson at a time. The optional reference library contains every text page in the pinned MDN Web/HTTP collection, plus six supporting pages. Search finds both lesson titles and slide text. Reference reading never blocks the final assessment.'),
      ('How to study','Predict a request’s method, headers, body and outcome. Inspect a real request, then explain what happened. Each guided lesson has practice and a worked check. Exercises are self-assessed; quizzes provide study feedback. Mark completion after viewing all slides. Retakes are allowed; passing is 80%.'),
      ('Scope and sources','The freeCodeCamp handbook supplies a topic checklist, with original explanations and examples grounded in MDN. Its article is linked, not republished. MDN’s licensed documentation is packaged as optional reference slides, including experimental/deprecated material with source notices. Generated compatibility tables and diagrams link to their sources. Full IETF specifications and linked third-party manuals are outside this snapshot.'),
      ('Your workspace','Progress and notes save in this browser. Reports are personal feedback, not exam-secure grades. Copy entire course includes the guided path, the complete optional reference, quizzes and answers; that export is large. Use the local practice server when a lesson calls for a reproducible request. The slide reader itself does not execute examples.')],
      'Choose one five-minute study session: read a lesson, predict a request, then take one skill check.',
      'Use the core path for progression and the optional reference for lookup. You do not need to memorize hundreds of header names.', ['Web/HTTP'])
    handbook=D('handbook-map','Handbook reading map','Connect all handbook topics to this course.',[
      ('Read alongside the course',f'Lane Wagner’s [HTTP Networking handbook]({HANDBOOK}) covers client/server exchanges, Fetch, DNS, URI/URL structure, asynchronous JavaScript, failures, headers, JSON bodies, methods/statuses, resource paths/query parameters and HTTPS. This course provides corresponding lessons and extends them using MDN.'),
      ('Use precise terminology','The guided course uses 401 Unauthorized for missing/invalid authentication and 403 Forbidden for refused access. DNS usually starts with a recursive resolver and caches; clients do not contact root servers for every lookup. Browser scripts cannot set every header. HTTPS protects transport but does not make a site trustworthy or anonymous.')],
      'Open the handbook section corresponding to the lesson you are studying. Compare one example with the relevant MDN reference.',
      'Use the handbook for a friendly introduction, then MDN for the detailed contract and browser restrictions. The source manifest maps every technical top-level handbook topic to lesson IDs.', ['Web/HTTP/Guides/Overview'])

    exchange=D('exchange','The request–response exchange','Identify what HTTP moves between participants.',[
      ('Representations travel','A client requests a resource representation, and a server responds. A page commonly triggers many requests for HTML, styles, scripts, images and data. HTTP can carry many media types; it does not require JSON.'),
      ('A concrete exchange','```http\nGET /lessons HTTP/1.1\nHost: localhost:8000\nAccept: application/json\n\n```\n\n```http\nHTTP/1.1 200 OK\nContent-Type: application/json\n\n{"lessons":[{"id":"syntax","title":"HTTP messages"}]}\n```\n\nThe blank line separates metadata from content in this HTTP/1.1 illustration. Length/framing headers are omitted for teaching.')],
      'Name the requester, target, method, response status and response body above.',
      'The client requests /lessons using GET. The server replies 200 with a JSON representation. A status line is not part of that JSON body.', ['Web/HTTP/Guides/Overview','Web/HTTP/Guides/Messages'])
    roles=D('roles','Clients, origins and intermediaries','Trace a request through more than one machine.',[
      ('Roles rather than permanent identities','A program may act as a server for one exchange and a client for another. The origin server is responsible for a resource; proxies, gateways and caches can sit between the client and origin.'),
      ('Stateless protocol, stateful applications','HTTP request semantics do not require remembering every preceding exchange. Applications can still store accounts, documents and sessions. A cookie or authorization field supplies context on a new request; stateless does not mean no database.'),
      ('Useful consequences','Caching can answer without contacting the origin. Reverse proxies can route traffic. Each intermediary introduces its own trust, cache and connection considerations. HTTP transport details do not define a business API contract.')],
      'A browser requests a course through a CDN and reverse proxy. Which hop might answer from cache?',
      'An eligible cache, including a CDN cache, may answer. The origin need not run for every cache hit. Each hop must respect cache rules and trust boundaries.', ['Web/HTTP/Guides/Overview','Web/HTTP/Guides/Proxy_servers_and_tunneling'])
    dns=D('dns','DNS and reaching a host','Separate resolving a hostname from an HTTP request.',[
      ('Names to addresses','DNS records describe names and services. Address records such as A and AAAA can provide IP addresses for a hostname. An address can serve many hostnames; a hostname can have several addresses. A subdomain need not correspond to a different physical machine.'),
      ('Resolvers and caches','A client generally asks a recursive resolver. Cached answers may be reused according to their TTL. On a cache miss, resolution may involve root, top-level-domain and authoritative servers. DNS resolution does not select an HTTP path.'),
      ('One diagnostic distinction','A DNS failure occurs before receiving an HTTP status from the target server. A 404 shows an HTTP-speaking server answered. Proxies and cached DNS can complicate the route; use evidence rather than guessing.')],
      'Compare a hostname lookup failure with GET /missing returning 404.',
      'The lookup failure prevents finding/reaching the named service; the 404 is an application-layer response after a server was reached.', ['Glossary/DNS','Web/HTTP/Guides/Session'])
    url=D('url-parts','URI, URL, scheme, authority and fragment','Read a URL without assuming every part is sent to the server.',[
      ('Identifiers and locations','A URI identifies a resource. URLs provide location/access information; URNs identify names in a namespace. For HTTP URLs, parse the scheme, hostname, effective port, path, query and fragment. Different URI schemes have different syntax; mailto is not an HTTP authority URL.'),
      ('Let a parser do the work','```js\nconst u = new URL("https://learn.example:8443/courses/7?view=summary#quiz");\nconsole.log(u.protocol); // https:\nconsole.log(u.hostname); // learn.example\nconsole.log(u.port); // 8443\nconsole.log(u.pathname); // /courses/7\nconsole.log(u.searchParams.get("view")); // summary\nconsole.log(u.hash); // #quiz\n```'),
      ('Defaults and credentials','HTTP and HTTPS commonly use default ports 80 and 443. URL.port may be empty for the default port. A fragment is handled by the client and is not part of the HTTP request target. Do not put passwords or tokens into URLs; URLs can appear in history and logs.')],
      'For the example, write the HTTP origin and the path/query request target.',
      'Origin: https://learn.example:8443. Target: /courses/7?view=summary. The #quiz fragment is not sent to the server.', ['Web/API/URL','Web/HTTP/Guides/Session'])
    query=D('query-path','Paths, queries and encoding','Build request URLs without unsafe concatenation.',[
      ('The server defines meaning','A path may map to a file, a routed handler or another resource. Query fields can select filters, sorting and pagination. Read the server’s contract; HTTP does not dictate what a field named limit means.'),
      ('Encode data as data','```js\nconst u = new URL("http://localhost:8000/lessons");\nu.searchParams.set("q", "cache & cookies");\nu.searchParams.set("limit", "2");\nconsole.log(u.searchParams.get("q")); // cache & cookies\n```\n\nURLSearchParams handles serialization. Treat an encoded separator inside a value differently from a separator between fields.'),
      ('Location is not permission','A guessed ID or path does not grant access. Query parameters may be repeated; application parsers decide how that is handled. Sensitive material can leak through URL logs even when transport uses HTTPS.')],
      'Add tag=http and tag=cache to a URL, then read them with getAll.',
      'Use searchParams.append twice and getAll("tag"). The server must document whether repeated tags are supported. Authorization belongs to trusted application logic.', ['Web/API/URL','Web/HTTP/Guides/Session'])

    messages=D('messages','Read HTTP messages','Distinguish semantic fields from wire-version formatting.',[
      ('HTTP/1.1 anatomy','The request line contains method, target and version. The response status line contains version, status and reason phrase. Headers follow, then a blank line and optional content. Bytes and framing rules determine message boundaries, not indentation.'),
      ('New versions, same core semantics','HTTP/2 and HTTP/3 use binary framing and pseudo-headers rather than transmitting HTTP/1.1 status/request lines in the same form. Tools may show a friendly reconstructed view. A status code and content type still have meaning across versions.'),
      ('Bodies are not guaranteed','HEAD responses and statuses such as 204 and 304 have no response content. A GET body has no generally defined semantics and browser Fetch rejects GET/HEAD bodies. Do not call response.json() automatically for every response.')],
      'Why can parsing a successful 204 response as JSON fail?',
      '204 has no response content. Success status and JSON body availability are separate questions. Handle bodyless outcomes before parsing.', ['Web/HTTP/Guides/Messages','Web/HTTP/Reference/Status/204'])
    headers=D('header-basics','Headers and the Headers API','Read and set permitted metadata intentionally.',[
      ('Names and values','Header field names are case-insensitive; each field defines its own value syntax. Not all duplicate fields combine the same way. Content-Type describes the representation sent; Accept describes formats the receiver would prefer.'),
      ('Use Headers','```js\nconst headers = new Headers();\nheaders.set("Accept", "application/json");\nconsole.log(headers.get("accept")); // application/json\nheaders.delete("Accept");\n```\n\nRequest.headers and Response.headers expose header collections with browser restrictions.'),
      ('Browser-controlled fields','Browsers manage fields such as Cookie, Host and many Sec-* headers. You cannot reliably override them from ordinary scripts. Cross-origin response headers may not be readable unless CORS exposes them. Setting Content-Type on a bodyless GET is usually unnecessary and may trigger a preflight.')],
      'Choose Accept or Content-Type: you request JSON; you upload JSON.',
      'For preference, use Accept: application/json. For a JSON request body, use Content-Type: application/json. A server need not satisfy every preference.', ['Web/HTTP/Reference/Headers','Web/HTTP/Guides/Content_negotiation','Web/API/Fetch_API/Using_Fetch'])
    bodies=D('body-formats','Representations: JSON, text, forms and XML','Keep HTTP content separate from the data format.',[
      ('HTTP does not choose JSON','Content-Type can describe JSON, HTML, text, images, XML or multipart data. Choose a parser appropriate to the response representation. JSON is text encoding structured values, not a guarantee that a business payload is correct.'),
      ('Sending and reading JSON','```js\nasync function createLesson() {\n  const response = await fetch("/lessons", {\n    method: "POST",\n    headers: { "Content-Type": "application/json", "Accept": "application/json" },\n    body: JSON.stringify({ title: "Messages" })\n  });\n  if (!response.ok) throw new Error(`HTTP ${response.status}`);\n  return response.json();\n}\n```\n\nThis illustrative call requires the local practice server. A parsed value still needs application validation.'),
      ('Other formats and encoding','XML uses markup and may be required by a service; JSON uses values/containers. HTML forms often use URL-encoded or multipart representations. With FormData, let the browser set the multipart boundary. Character encoding, media type and compression are separate ideas. The JSON LMS teaches the format in detail.')],
      'Explain why sending a plain JavaScript object as fetch body does not automatically create correct JSON.',
      'Serialize the intended representation explicitly. The header labels bytes; it does not convert an object into JSON. response.json() returns parsed data rather than a JSON string.', ['Web/HTTP/Guides/MIME_types','Web/API/Fetch_API/Using_Fetch'])
    negotiate=D('negotiate','Content negotiation and compression','Explain how a representation varies between requests.',[
      ('Preferences and metadata','Accept, Accept-Language and Accept-Encoding can communicate preferences for media type, language and content encoding. The response describes the chosen representation. Servers decide which variants they can produce.'),
      ('Vary protects variant caches','A cache needs to know which request fields influenced selection. Vary: Accept-Encoding tells a cache not to reuse a compressed variant blindly for a client with a different encoding capability.'),
      ('Compression is another layer','Content-Encoding describes a coding applied to the representation, such as gzip or br. It differs from Content-Type. Compression dictionary transport and emerging mechanisms belong in the optional reference; check live compatibility before using them.')],
      'A server selects language using Accept-Language. What should the response communicate to caches?',
      'Include the appropriate Vary information and response representation metadata, such as Content-Language. The policy must match the server’s actual variant selection.', ['Web/HTTP/Guides/Content_negotiation','Web/HTTP/Guides/Compression','Web/HTTP/Reference/Headers/Vary'])

    methods=D('method-contracts','Safe and idempotent methods','Predict intended effects, not just verb spelling.',[
      ('Safe means a read-only intended action','GET and HEAD request information. OPTIONS asks about capabilities. Safe methods should not request a state change, although logging and incidental effects can occur. Never make GET trigger a purchase or deletion.'),
      ('Idempotent means the intended effect stabilizes','Repeating an identical idempotent request has the same intended effect as one request. PUT and DELETE are idempotent by semantics; repeated responses can differ. Idempotence is not a guarantee of identical status codes or no incidental logging.'),
      ('Other methods and extensions','HEAD resembles GET without response content. OPTIONS can participate in CORS preflight. CONNECT establishes a tunnel; TRACE is diagnostic and often disabled. The optional method reference includes newer or experimental methods such as QUERY; do not assume every server/browser supports them.')],
      'A DELETE succeeds once, then returns 404 on retry. Does the changed status alone violate idempotence?',
      'No. If the intended result is that the target association is removed, the effect can be idempotent while responses differ. Whether to retry depends on the complete contract.', ['Web/HTTP/Reference/Methods','Web/HTTP/Reference/Methods/HEAD','Web/HTTP/Reference/Methods/DELETE'])
    writes=D('write-methods','POST, PUT, PATCH and DELETE','Choose write semantics deliberately.',[
      ('POST processes submitted content','POST often creates a subordinate resource or triggers processing, but HTTP does not equate it exclusively with database creation. Repeating a POST can have additional effects unless the application supplies a deduplication contract.'),
      ('PUT replaces; PATCH applies changes','PUT creates or replaces the target representation and is idempotent. PATCH applies a partial modification described by its patch media type; it is not inherently safe or idempotent. A patch that sets a value and one that increments a value have different retry risks.'),
      ('DELETE and concurrency','DELETE requests removal of the target association; physical storage behavior is an implementation detail. Preconditions such as If-Match can protect an update against stale data. The server must enforce business and access rules.')],
      'Compare sending an entire lesson with PUT and applying an increment operation with PATCH.',
      'Repeating the same PUT should produce the same intended representation. Repeating an increment patch may increment again. A retry policy must consider this difference.', ['Web/HTTP/Reference/Methods/POST','Web/HTTP/Reference/Methods/PUT','Web/HTTP/Reference/Methods/PATCH'])
    statuses=D('status-families','Status codes and failure categories','Read status meanings without memorizing the entire reference.',[
      ('Five families','1xx communicates interim information; 2xx success; 3xx redirection or cache-related outcomes; 4xx a request cannot be fulfilled under client-facing conditions; 5xx server-side failure. A family gives context, but the specific code matters.'),
      ('Common outcomes','200 OK carries the applicable success result. 201 Created indicates creation; Location can identify the new resource. 202 Accepted does not mean work has completed. 204 No Content has no response content. 304 supports conditional cache reuse rather than an ordinary document redirect.'),
      ('Troubleshooting distinctions','400 Bad Request differs from 415 Unsupported Media Type. 401 Unauthorized concerns authentication; 403 Forbidden means refusal. 404 can also deliberately conceal a resource. 405 identifies unsupported methods with Allow. 429 indicates rate limiting; 502/504 concern gateway failures.')],
      'A job submission returns 202. Should the UI immediately announce the job is finished?',
      'No. It was accepted, not necessarily completed. Use the server’s documented status-monitoring mechanism. Do not treat all 2xx responses as identical.', ['Web/HTTP/Reference/Status','Web/HTTP/Reference/Status/202','Web/HTTP/Reference/Status/401','Web/HTTP/Reference/Status/403'])
    redirects=D('redirects','Redirects and method preservation','Follow a changed location without silently changing meaning.',[
      ('Location and permanence','Location communicates a redirect target. 301 and 308 describe permanent movement; 302 and 307 temporary movement. Permanent redirects can be cached, making a mistaken configuration difficult to undo immediately.'),
      ('Method changes matter','303 directs retrieval of another resource, commonly using GET after a POST. 307 and 308 preserve method and body. Historical handling of 301/302 can change a POST to GET. For reliable behavior, choose the status for the intended contract.'),
      ('Client behavior and risks','Fetch normally follows redirects automatically. Inspect redirect chains and final URLs when debugging. Do not forward secrets indiscriminately to new origins; protect against redirect loops and open-redirect application flaws.')],
      'A server needs a client to repeat a POST temporarily at another URL. Which redirect is appropriate?',
      '307 preserves method/body and describes temporary movement. 303 would instead direct a retrieval request; the server contract should make the choice explicit.', ['Web/HTTP/Guides/Redirections','Web/HTTP/Reference/Status/307','Web/HTTP/Reference/Status/303'])
    resources=D('resource-contracts','HTTP and a resource API contract','Recognize what HTTP leaves to the application.',[
      ('Contract beyond the transport','The API documents its base URL, paths, methods, parameters, representations and outcomes. HTTP does not specify what a /courses endpoint means. REST is an architectural style, not a different HTTP wire protocol.'),
      ('Language independence and state','A client and server can use different languages while agreeing on messages. A stateless interaction includes the needed request context; servers may still store resource state. Naming paths after resources is a useful convention, not proof of every REST constraint.'),
      ('Keep the course focused','This course teaches transport semantics and diagnostics. API design, data modeling, pagination strategy, authorization architecture and service governance belong in the API LMS. Use the HTTP reference when assessing the transport choices.')],
      'List what you need from documentation before calling an unfamiliar endpoint.',
      'At minimum: target/base URL, method, required parameters, representation/content type, credentials/access rules and expected responses. Check errors and retry behavior too.', ['Web/HTTP/Guides/Overview','Web/HTTP/Reference/Methods'])

    asyncdeck=D('async-flow','Promises, callbacks and async/await','Trace asynchronous requests without blocking the UI.',[
      ('Pending, fulfilled or rejected','A Promise represents an eventual outcome. A then handler processes fulfillment; catch handles rejection. An async function returns a Promise. Await suspends that async function until the outcome; it does not freeze the whole browser or make all code parallel.'),
      ('Predict the order','```js\nconsole.log("start");\nPromise.resolve("data").then(value => console.log(value));\nconsole.log("after");\n// start, after, data\n```\n\nCallbacks also underpin timers and events. Async work can overlap, but JavaScript execution and CPU parallelism are separate concepts.'),
      ('A missing await changes the value','```js\nasync function readLessons() {\n  const response = await fetch("/lessons");\n  if (!response.ok) throw new Error(`HTTP ${response.status}`);\n  return response.json();\n}\n// await readLessons() gives data; readLessons() gives a Promise.\n```'),
      ('Create a Promise only when needed','```js\nconst delay = ms => new Promise(resolve => setTimeout(resolve, ms));\nasync function demo() {\n  await delay(10);\n  return "ready";\n}\n```\n\nDo not wrap fetch in a new Promise just to use it. Returning a then chain or using await usually composes the existing Promise.')],
      'Predict whether try { fetch("/missing") } catch {} waits for or catches a rejected Promise.',
      'It does not await the Promise. Use await inside try/catch, or attach a rejection handler. Also, an HTTP 404 normally resolves fetch rather than rejecting it.', ['Web/JavaScript/Reference/Global_Objects/Promise','Web/JavaScript/Reference/Operators/await','Web/JavaScript/Reference/Statements/async_function'])
    fetch=D('fetch-basics','Make a request with Fetch','Construct a request and consume its body intentionally.',[
      ('Separate response metadata from content','Fetch resolves with a Response after the response is available. The response exposes status, ok, headers and body-reading methods. Reading a JSON/text body is another asynchronous operation.'),
      ('A small client function','```js\nasync function load(url) {\n  const response = await fetch(url, { headers: { Accept: "application/json" } });\n  if (!response.ok) throw new Error(`HTTP ${response.status}`);\n  if (response.status === 204) return null;\n  return response.json();\n}\n```\n\nRun with the local practice server and /lessons. Validate the returned shape if the application depends on it.'),
      ('One body, one consumption','A body is a stream. A second read generally fails once it is consumed. If two consumers truly need a response, clone it before the first read, considering memory/backpressure. Browser Fetch controls request/response headers and stream behavior beyond bare HTTP semantics.')],
      'Why is JSON.parse(await response.json()) usually wrong?',
      'response.json() already parses JSON text to a value. If you need text, read response.text() then parse deliberately; do not parse a parsed object again.', ['Web/API/Fetch_API/Using_Fetch'])
    errors=D('fetch-errors','Network errors, HTTP errors and parsing errors','Handle the layer that actually failed.',[
      ('Fetch does not reject for every bad status','A 404 or 500 normally produces a Response. Test response.ok/status and implement the application’s error policy. A failed connection, blocked browser policy or abort may reject before you can inspect a useful response.'),
      ('Await inside try/catch','```js\nasync function inspect(url) {\n  try {\n    const response = await fetch(url);\n    if (!response.ok) return { kind: "http", status: response.status };\n    if (response.status === 204) return { kind: "empty" };\n    return { kind: "ok", data: await response.json() };\n  } catch (error) {\n    return { kind: "request-or-parse", message: error.message };\n  }\n}\n```\n\nA production UI should distinguish categories more precisely when it has evidence.'),
      ('Handling and debugging work together','An offline device is an expected runtime condition. A wrong endpoint or forgotten await is a bug to fix. A malformed body may indicate a server error or wrong parser. Catching an exception does not fix the underlying logic; inspect the status, content type and body safely.')],
      'Test /missing, /empty and /invalid-json on the local practice server. Predict the categories before running.',
      'They yield an HTTP 404 result, a bodyless successful result and a parse rejection respectively. A 200 status does not prove the body is valid JSON.', ['Web/API/Fetch_API/Using_Fetch','Web/HTTP/Reference/Status'])
    abort=D('abort-retry','Abort, timeouts and careful retries','Cancel client work without assuming the server rolled back.',[
      ('Cancellation','```js\nasync function bounded(url) {\n  const controller = new AbortController();\n  const timer = setTimeout(() => controller.abort(), 50);\n  try { return await fetch(url, { signal: controller.signal }); }\n  finally { clearTimeout(timer); }\n}\n```\n\nThis bounds waiting for fetch to resolve. If you also need a bound on reading the body, keep the timeout active through body consumption.'),
      ('A lost response is ambiguous','Aborting a request is not a server transaction rollback. A write may have committed before the response was lost. Retrying non-idempotent operations can duplicate effects. Follow the documented application contract.'),
      ('Bound retries','Limit attempts and total waiting. Consider backoff/jitter, Retry-After, cancellation and whether the operation is safe to repeat. Do not retry authentication failures or malformed payloads endlessly.')],
      'You submit a purchase, then time out before reading the response. Can you assume it failed?',
      'No. The server may have completed the operation. Consult the transaction/idempotency contract or an explicit status endpoint rather than automatically creating another purchase.', ['Web/API/Fetch_API/Using_Fetch','Web/HTTP/Reference/Headers/Retry-After'])
    inspect=D('inspect-network','Use the Network panel and curl','Collect evidence about the actual exchange.',[
      ('Browser checklist','Open developer tools, select Network, then reload or perform the action. Inspect URL, method, status, request headers, response headers, content, timing, redirects and initiator. Disable cache only when you intend to test that condition.'),
      ('Command-line inspection','```sh\ncurl -i http://localhost:8000/lessons\ncurl -I http://localhost:8000/lessons\ncurl -i -H \'If-None-Match: "lesson-v1"\' http://localhost:8000/etag\n```\n\nThe first displays response headers/body; the second sends HEAD. Browser and command-line clients have different policy restrictions.'),
      ('Protect captured data','Request headers, cookies, URLs and HAR exports can contain secrets. Redact before sharing. A curl request succeeding while browser Fetch fails can point toward CORS/browser policy; it does not prove permission to bypass the server’s rules.')],
      'Inspect /redirect and /etag in the local practice server. Record the first status and final outcome.',
      'The redirect returns 303 with Location /lessons; a client may follow it. /etag returns 200 and ETag, then 304 for the matching If-None-Match value. Inspect intermediate responses rather than only the final view.', ['Web/HTTP/Guides/Session','Web/HTTP/Guides/CORS'])

    cookies=D('cookies','Cookies and session state','Explain how an application carries context between requests.',[
      ('Set and send','The server sets cookies with Set-Cookie; the browser sends applicable cookies with Cookie. Domain, Path, expiry and other attributes govern their scope/lifetime. The application decides what a session identifier means.'),
      ('Attributes have different purposes','Secure restricts sending to secure transport, with localhost-specific browser behavior. HttpOnly prevents script access through document.cookie; it does not prevent every attack. SameSite controls certain cross-site sending. SameSite=None requires Secure in modern browsers. Consider host-only cookies and cookie prefixes where appropriate.'),
      ('Credentials and privacy','Fetch credentials mode influences cookie sending and acceptance. Browsers also enforce third-party cookie restrictions. Cookies are not proof of authorization by themselves, and client storage is not a place to casually expose secrets.')],
      'Explain why adding HttpOnly does not turn an insecure HTTP deployment into HTTPS.',
      'HttpOnly protects a script-access boundary. Transport encryption is provided by HTTPS; the attributes solve different problems.', ['Web/HTTP/Guides/Cookies','Web/HTTP/Reference/Headers/Set-Cookie'])
    auth=D('authentication','Authentication and access outcomes','Distinguish identifying a caller from granting an operation.',[
      ('Challenge and response','A server may send 401 with WWW-Authenticate to challenge authentication. A client may provide Authorization. A proxy has a separate 407 challenge mechanism. Different schemes have different security requirements.'),
      ('Identity is not permission','Authentication identifies or verifies a caller. Authorization decides whether that caller may do an action or access a resource. 403 means refusal even though authentication may have been provided. Servers may use 404 to avoid revealing a protected resource.'),
      ('Do not expose credentials','Basic authentication encodes credentials; base64 is not encryption. Use HTTPS and an appropriate scheme. Do not ship server secrets inside a static LMS or frontend bundle. Treat example credentials as illustrative, not real permissions.')],
      'A user is signed in but cannot access another person’s report. Is that mainly an authentication or authorization question?',
      'Authorization: a valid identity does not imply access to every object. The server must enforce the rule on each protected operation.', ['Web/HTTP/Guides/Authentication','Web/HTTP/Reference/Headers/Authorization'])
    cors=D('cors','Same origin, CORS and preflight','Explain what a browser allows a script to read.',[
      ('Origin is a tuple','For ordinary HTTP origins, scheme, hostname and port matter. Different paths on the same origin do not create different origins. Cross-origin reading is constrained by browser policy; CORS lets a server opt into specified sharing.'),
      ('Preflight is conditional','Certain cross-origin methods/headers/content types require an OPTIONS preflight before the actual request. The browser asks whether the method and headers are allowed. A safelisted request may be sent without preflight even when its response cannot be read.'),
      ('Credentials and limits','Credentialed sharing cannot use a wildcard Access-Control-Allow-Origin. Allowed origins and credentials must match policy. CORS is not server authorization and does not by itself prevent CSRF. mode:no-cors gives an opaque response rather than readable data or permission to ignore security.')],
      'Why might curl read a response while browser Fetch reports a CORS problem?',
      'CORS is a browser sharing policy. Inspect the request Origin, preflight if present, and response allow/expose fields. A command-line success does not change what a browser script is allowed to read.', ['Web/HTTP/Guides/CORS','Web/HTTP/Guides/CORS/Errors'])

    cache=D('cache-freshness','Caching: freshness and storage','Predict whether a cache may reuse a representation.',[
      ('Private and shared caches','A browser cache and a shared/CDN cache have different audiences. Cache-Control directives govern storage and reuse. A personalized representation should not be accidentally shared between users.'),
      ('Common directives','max-age bounds freshness. s-maxage targets shared caches. private prohibits shared-cache storage. no-store says not to store. no-cache permits storage but requires validation before reuse. The names no-cache and no-store are not interchangeable.'),
      ('Stable URLs and variants','Versioned asset URLs can support long-lived caching. Representation variation may require Vary. Freshness calculations also consider age and timestamps; caches are more than a local Map with a timer.')],
      'Choose no-store or no-cache: a sensitive response must not be stored; a reusable response must be revalidated.',
      'Use no-store for the storage restriction. Use no-cache for required validation before reuse. Other privacy/application controls can still be necessary.', ['Web/HTTP/Guides/Caching','Web/HTTP/Reference/Headers/Cache-Control'])
    validators=D('validators','Conditional requests and validators','Reuse unchanged data and protect stale updates.',[
      ('Revalidate a cached representation','An ETag identifies a representation version according to server rules. A cache/client can send If-None-Match; if it matches, a GET may receive 304, reusing its stored content. Last-Modified and If-Modified-Since provide a timestamp-based mechanism.'),
      ('Preconditions on writes','If-Match can require a matching representation before applying a write. A failed precondition can return 412. This helps avoid a lost update when two editors work from stale data, but the server must implement it correctly.'),
      ('Strong and weak validators','A weak ETag does not assert byte-for-byte equality. Different conditional operations have different comparison requirements. Treat validators as opaque server-issued values rather than guessing them.')],
      'A client sends If-None-Match for a stored response and receives 304. Where does the displayed body come from?',
      'The existing cached representation, after applying the response’s relevant metadata. The 304 response itself carries no new representation body.', ['Web/HTTP/Guides/Conditional_requests','Web/HTTP/Reference/Headers/ETag'])
    ranges=D('ranges','Range requests and large resources','Retrieve part of a representation using the server contract.',[
      ('Partial transfer','Range requests can ask for byte ranges. A supported satisfiable request can produce 206 Partial Content with Content-Range. A server may ignore Range and return a complete 200; clients must handle the actual outcome.'),
      ('Unsatisfied and conditional ranges','An unsatisfiable range can return 416. Accept-Ranges advertises support. If-Range can request a partial transfer only when the representation still matches a validator, otherwise obtaining the full representation.'),
      ('Multiple ranges and practical limits','Multiple ranges can use a multipart response. Validate boundaries, lengths and response metadata rather than assuming a download resume succeeded. Range behavior is distinct from application-level pagination.')],
      'Would a 200 response to a Range request always prove the server sent only the requested bytes?',
      'No. Inspect status and Content-Range. A 200 can be the full representation. 206 signals a fulfilled partial-content response.', ['Web/HTTP/Guides/Range_requests','Web/HTTP/Reference/Status/206','Web/HTTP/Reference/Status/416'])

    https=D('https','HTTPS, TLS and mixed content','Describe transport protection and its limits.',[
      ('What TLS protects','HTTPS uses TLS to protect confidentiality and integrity in transit and authenticate the server according to the certificate/trust model. Modern deployments use TLS rather than obsolete SSL. HTTP/3 integrates TLS protection with QUIC.'),
      ('What it does not promise','HTTPS does not guarantee that an operator is honest, that application authorization is correct, or that the user is anonymous. Endpoints see the content; traffic metadata can still be observable. Encrypting transport does not fix a data leak inside the application.'),
      ('Browser policies','An HTTPS document loading insecure resources can encounter mixed-content blocking or upgrades. HSTS asks browsers to use secure connections for future access under its rules. Misconfigured HSTS/preload can affect an entire deployment; understand scope before applying it.')],
      'A phishing site has a valid HTTPS certificate. Does that establish the site is trustworthy?',
      'No. It establishes the transport/server identity under the certificate model, not the legitimacy of every claim or business action.', ['Web/HTTP/Guides/Overview','Web/HTTP/Reference/Headers/Strict-Transport-Security','Web/HTTP/Reference/Headers/Upgrade-Insecure-Requests'])
    policies=D('browser-policies','CSP, framing and browser isolation','Find the right policy for a specific browser boundary.',[
      ('Content Security Policy','CSP can restrict permitted sources for scripts, styles, frames and connections. Directives have distinct roles and fallback rules. Report-only policy helps observe violations before enforcement; it does not enforce the same blocking rules.'),
      ('Other boundaries','frame-ancestors controls which parents may embed a page. Referrer-Policy controls referrer disclosure. X-Content-Type-Options:nosniff constrains certain MIME interpretations. CORP, COEP and COOP address different resource/embedding/opener boundaries; they do not all mean CORS.'),
      ('Use the reference carefully','Permissions Policy delegates or restricts specific browser capabilities. Experimental, deprecated and non-standard directives remain in the reference with notices. Do not paste every security header into a site blindly; policy can break legitimate features.')],
      'You want to observe a proposed CSP without blocking production features immediately. Which form helps?',
      'Content-Security-Policy-Report-Only can collect reports for supported behavior. Review the reports and policy before switching to enforcement.', ['Web/HTTP/Guides/CSP','Web/HTTP/Guides/Permissions_Policy','Web/HTTP/Guides/Cross-Origin_Resource_Policy'])
    proxy=D('proxy-trust','Proxies, forwarding and origin trust','Interpret forwarding metadata without trusting arbitrary claims.',[
      ('Forward and reverse proxies','A forward proxy acts on behalf of a client; a reverse proxy/gateway fronts a service. Tunneling and CONNECT differ from simply forwarding an ordinary HTTP request. A path may involve several independently managed hops.'),
      ('Forwarded metadata','Forwarded and X-Forwarded-* fields can communicate earlier client/protocol/host information. They are not inherently trustworthy: an attacker may send similar fields. A deployment needs a trusted-proxy configuration and a rule for sanitizing incoming values.'),
      ('Observability and privacy','Via and Server-Timing can support diagnostics. Network error logging, Fetch Metadata and client hints have specialized roles and support constraints. Prefer feature detection over brittle user-agent string parsing where possible.')],
      'A public client sends X-Forwarded-Proto:https directly to your HTTP server. Can that alone establish a secure original connection?',
      'No. Trust only metadata from the configured proxy boundary, applying the server framework’s trusted-proxy rules. A client-supplied field is just a claim.', ['Web/HTTP/Guides/Proxy_servers_and_tunneling','Web/HTTP/Reference/Headers/Forwarded','Web/HTTP/Guides/Browser_detection_using_the_user_agent'])

    versions=D('versions','HTTP/1.1, HTTP/2 and HTTP/3','Connect performance changes to stable message semantics.',[
      ('HTTP/1.x connections','Persistent connections reduce repeated setup. HTTP/1.x connection management has limits, including ordering and head-of-line concerns. Browsers manage connection reuse; a fetch option is not a raw TCP socket controller.'),
      ('HTTP/2','HTTP/2 multiplexes streams on a connection and compresses header metadata. It changes framing while preserving HTTP semantics. TCP-level loss can still affect multiple streams sharing a connection.'),
      ('HTTP/3','HTTP/3 runs over QUIC rather than a TCP connection, with TLS integration and stream behavior that reduces transport head-of-line blocking between independent streams. It does not eliminate latency, congestion or application-level dependencies.'),
      ('Upgrade and negotiation','Protocol negotiation/upgrade mechanisms vary. HTTP/1.1 Upgrade can switch protocols in specific situations; WebSocket handshakes and tunneled traffic are related mechanisms, not interchangeable with every HTTP version upgrade.')],
      'Does moving to HTTP/2 turn a POST into an idempotent request?',
      'No. Wire framing and multiplexing do not redefine the method’s intended semantics. Retry safety still depends on method and application contract.', ['Web/HTTP/Guides/Evolution_of_HTTP','Web/HTTP/Guides/Connection_management_in_HTTP_1.x','Web/HTTP/Guides/Protocol_upgrade_mechanism'])
    capstone=D('capstone','Project: diagnose a lesson client','Combine inspection, status handling, caching and safe retries.',[
      ('Run a local fixture','Run node scripts/practice-server.cjs and open http://localhost:8000. This serves the LMS and synthetic practice endpoints on loopback. Use curl or the browser console. Stop with Ctrl+C. It is a teaching fixture, not a production service.'),
      ('Required evidence','Record exchanges for /lessons, /missing, /empty, /invalid-json, /redirect, /etag and /slow. For each: method, status or failure, relevant headers, body/parser decision and a user-facing outcome. Make a JSON POST to /lessons and inspect 201/Location.'),
      ('Two client improvements','Write a bounded client that handles non-2xx, 204 and malformed JSON separately. Revalidate /etag with its ETag. Explain which requests you would retry, how you would avoid indefinite waiting, and why aborting a write is ambiguous.'),
      ('Self-review rubric','Award 0–2 for message reading, URL construction, method semantics, status handling, parser choice, cancellation, conditional caching and clear diagnostics. Aim for 13/16. The LMS does not automatically grade your implementation.')],
      'Write a one-page diagnosis and show one failing fixture plus its deliberate handling.',
      '/missing is an HTTP 404; /invalid-json is a successful status with malformed JSON; /empty is a bodyless 204. /etag responds 304 only when the validator matches. /slow demonstrates client cancellation. Their failure layers require different handling.', ['Web/HTTP/Guides/Messages','Web/API/Fetch_API/Using_Fetch'])

    sections=[
      module('m1','01 Start here',[start,handbook]),
      module('m2','02 How HTTP reaches a resource',[exchange,roles,dns,url,query],'HTTP foundations',[
        ('Which URL component is not sent as the HTTP request target?',['Path','Fragment','Query'],1,'Fragments are handled by the client.'),
        ('What does DNS primarily help resolve here?',['A hostname to address information','The business meaning of /courses','A JSON field type'],0,'DNS and HTTP path routing are separate layers.'),
        ('Can an HTTP application store accounts while using stateless request semantics?',['No','Only over HTTP/3','Yes'],2,'Stateless interactions do not forbid resource or application state.')]),
      module('m3','03 Messages and representations',[messages,headers,bodies,negotiate],'Messages and headers',[
        ('Which field describes a sent JSON representation?',['Accept-Language','Content-Type','Location'],1,'Content-Type describes the representation being sent.'),
        ('What should a client expect for 204?',['No response content','A required JSON object','An HTML error page'],0,'204 is a bodyless success outcome.'),
        ('What does Vary communicate?',['A password rotation schedule','A request method alias','Which request fields affect representation selection'],2,'Caches need this information to select the correct variant.')]),
      module('m4','04 Methods and outcomes',[methods,writes,statuses,redirects,resources],'Method and status semantics',[
        ('Idempotence guarantees what?',['The same intended effect for repeated identical requests','The same response bytes','No incidental logging'],0,'Responses and logging can differ while the intended effect stabilizes.'),
        ('Which redirect preserves method/body temporarily?',['303','307','301'],1,'307 indicates temporary redirection with method preservation.'),
        ('What does 202 indicate?',['Completed background work','A required redirect','Acceptance without guaranteed completion'],2,'The client needs the documented completion/status mechanism.'),
        ('Which code concerns an authentication challenge?',['401','403','429'],0,'401 Unauthorized concerns missing/invalid authentication, usually with WWW-Authenticate.')]),
      module('m5','05 Fetch and debugging',[asyncdeck,fetch,errors,abort,inspect],'Client requests and diagnostics',[
        ('Does fetch normally reject just because a server returns 404?',['Yes','No; inspect status/ok','Only if the method is GET'],1,'HTTP error statuses generally produce a Response.'),
        ('What does an async function return?',['A Promise','An HTTP header','Only a synchronous primitive'],0,'Its eventual return or failure becomes a Promise outcome.'),
        ('Does aborting a write prove the server rolled it back?',['Yes','Only with JSON','No'],2,'The server may already have committed the operation.'),
        ('Where can you inspect redirect chains and actual headers?',['Only the page title','Browser Network tools','The JSON indentation'],1,'Network inspection reveals the actual exchange.')]),
      module('m6','06 State and browser access',[cookies,auth,cors],'State and cross-origin access',[
        ('What does HttpOnly mainly restrict?',['Script access to the cookie','All network traffic','All authenticated actions'],0,'It is a script-access boundary, separate from TLS and permission checks.'),
        ('Can CORS replace server authorization?',['Yes','No','Only for GET'],1,'Sharing policy and application permission are distinct.'),
        ('For credentialed cross-origin sharing, is wildcard Access-Control-Allow-Origin valid?',['Always','Only with a POST body','No'],2,'Credentialed responses require a specific allowed origin and applicable credentials policy.')]),
      module('m7','07 Caching and partial transfer',[cache,validators,ranges],'Caching and conditional requests',[
        ('What does no-cache generally require?',['No storage under any condition','Validation before reuse','Only compressed transfer'],1,'no-store is the storage restriction; no-cache requires validation.'),
        ('A matching If-None-Match GET can produce which result?',['304 with cached-content reuse','201 creation','307 movement'],0,'304 carries metadata for reusing the stored representation.'),
        ('What can If-Match help protect against?',['Every DNS failure','Every browser restriction','Updating from a stale representation'],2,'The server can reject an update whose precondition no longer matches.')]),
      module('m8','08 Transport and browser security',[https,policies,proxy],'HTTP security boundaries',[
        ('What does HTTPS provide?',['Proof that a business is honest','Protected transport and server authentication under the trust model','Guaranteed anonymity'],1,'Transport protection does not validate every application/business claim.'),
        ('What is report-only CSP useful for?',['Observing supported violations before enforcement','Replacing access control','Guaranteeing no script ever runs'],0,'Report-only policy is observational rather than the normal blocking enforcement.'),
        ('Should arbitrary client-supplied forwarding fields be trusted?',['Always','Only if the name begins X-','No; use a configured trusted-proxy boundary'],2,'Forwarding metadata is a claim unless trusted infrastructure supplies/sanitizes it.')]),
      module('m9','09 Versions and connections',[versions],'Protocol evolution',[
        ('Which transport is used by HTTP/3?',['QUIC','Only an HTTP/1.1 pipeline','A JSON parser'],0,'HTTP/3 runs over QUIC with TLS integration.'),
        ('Does HTTP/2 change the semantics of DELETE?',['Yes, it becomes unsafe to name it','No; framing and method semantics are separate','Yes, it becomes a GET'],1,'Version evolution preserves core HTTP semantics.')]),
      module('m10','10 Capstone and final review',[capstone])]
    final=[
      ('A URL ends in #chapter. Where is that part handled?',['By the client','In the Host header','As a required server JSON field'],0,'A fragment is not transmitted as the HTTP request target.'),
      ('A hostname cannot resolve. What would you expect before receiving a target HTTP status?',['A guaranteed 500','A resolution/connectivity failure','A successful JSON response'],1,'The failure can occur before an HTTP-speaking server answers.'),
      ('A browser requests two media types using Accept. What determines the sent format?',['The query string alone','The number of headers','The server selects and describes its representation'],2,'Accept is a preference; Content-Type describes the actual representation.'),
      ('A 204 response reaches your JSON client. What is the appropriate first handling?',['Treat it as bodyless success','Read a mandatory JSON object','Retry until there is text'],0,'204 has no response content.'),
      ('A repeated DELETE returns a different status but leaves the resource removed. What is the correct inference?',['Idempotence is necessarily broken','The intended effect can still be idempotent','DELETE must create a new record'],1,'Idempotence concerns intended effect rather than identical replies.'),
      ('A temporary redirect must retain a submitted body. Which status fits?',['303','302','307'],2,'307 preserves method and body.'),
      ('The browser Fetch Promise resolves to a Response with status 500. What must the application do?',['Inspect status/ok and handle the outcome','Assume the Promise rejection handler already ran','Parse the Response object with eval'],0,'HTTP failures normally still resolve fetch.'),
      ('An error arrives while awaiting response.json(). Which layer may have failed?',['DNS only','Body decoding/parsing','Only URL fragment handling'],1,'Body consumption can fail after a successful response status.'),
      ('A purchase request times out. What is unsafe to assume?',['The client stopped waiting','The outcome is uncertain','The purchase definitely never happened'],2,'The server might have committed the write before the response was lost.'),
      ('A script receives an opaque no-cors response. Can it freely read its JSON body?',['No','Yes, if it calls parse twice','Yes, if it changes indentation'],0,'no-cors is not a readable-data bypass.'),
      ('A shared cache serves personalized account data across users. Which lesson should guide the fix?',['Increase every cache lifetime','Correct cache audience/storage rules and application controls','Rename a URL fragment'],1,'Private/no-store policies and correct application boundaries protect sensitive representations.'),
      ('A saved representation revalidates with a matching ETag. Where can the content for a 304 outcome come from?',['The 304 body itself','A required POST upload','The stored cached representation'],2,'304 enables reuse of existing content with relevant updated metadata.'),
      ('Two editors work on the same lesson version. Which field can help reject a stale write?',['If-Match','Accept-Language','Server-Timing'],0,'A validator precondition can protect against overwriting a newer representation.'),
      ('A Range request receives 200 rather than 206. What must the client check?',['Only the request URL title','Whether the response is the complete representation','Whether all arrays are zero-based'],1,'The server may ignore Range and send the full representation.'),
      ('A site uses HTTPS but exposes another user’s report. What still needs correction?',['Only the font size','Only the HTTP version','Application authorization'],2,'TLS does not enforce object access rules.'),
      ('A client directly sets X-Forwarded-Proto:https. What should a server do?',['Trust only the configured proxy boundary','Automatically grant secure-session privileges','Treat it as a verified certificate'],0,'Untrusted metadata does not establish the transport history.'),
      ('A proposed CSP is in report-only mode. What should you expect?',['Every violation is necessarily blocked','Supported reports without ordinary enforcement blocking','It replaces authentication'],1,'Report-only supports observing a policy before enforcement.'),
      ('An application changes from HTTP/1.1 to HTTP/3. What remains necessary?',['Discard all status handling','Assume all writes can retry safely','Respect method/status semantics and application contracts'],2,'Changing framing/transport does not remove semantic or business requirements.')]
    return dict(schemaVersion=1,id='http-documentation-course-v1',title='HTTP',description='A focused HTTP learning path with original practice, assessments and the complete pinned MDN HTTP text reference collection. Covers the freeCodeCamp handbook topics while keeping full API and JSON courses separate.',sections=sections,settings=dict(passScore=80,allowRetakes=True,showLessonDetails=False,unlockAll=True,sequential=False,requireLessons=True,brand='#7bbcff',background='#0c0e12',surface='#14171d',text='#edf0f7',muted='#b4bac9',border='#343b49',fontScale=1,spacing=24,contentWidth=1000,radius=8,font='system',headingFont='system',lineHeight=1.65),finalQuiz=dict(id='http-final',type='quiz',title='Final assessment — HTTP skills',skill='HTTP integration',questions=[dict(id=f'final-q{i+1}',prompt=p,options=o,answer=a,explanation=e) for i,(p,o,a,e) in enumerate(final)]))
