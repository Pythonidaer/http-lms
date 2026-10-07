const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const course=JSON.parse(fs.readFileSync('course.json')),manifest=JSON.parse(fs.readFileSync('source-manifest.json')),inventory=JSON.parse(fs.readFileSync('docs/source-inventory.json'));
const context=vm.createContext({crypto});vm.runInContext(fs.readFileSync('lms-runtime.js','utf8')+';globalThis.courseAPI=LMS;',context);const valid=context.courseAPI.validate(course);
assert.equal(context.courseAPI.ready(valid).length,0);
const lessons=context.courseAPI.flatten(valid.sections),ids=new Set(lessons.map(n=>n.id));
assert.equal(lessons.filter(n=>n.optional).length,383);assert.equal(manifest.mdnHttpPages,377);assert.equal(manifest.sources.length,inventory.length);
for(const source of manifest.sources){const bytes=fs.readFileSync(source.sourcePath);assert.equal(crypto.createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${bytes.length}\0`),bytes])).digest('hex'),source.upstreamBlob);assert.ok(ids.has(source.lessonId));}
const embedded=fs.readFileSync('index.html','utf8').match(/<script id="lms-course-data" type="application\/json">(.*?)<\/script>/s)[1];assert.deepEqual(JSON.parse(embedded),course);
for(const n of lessons)for(const s of n.slides||[]){assert.ok(s.body.length<=20000,`${n.title} oversized`);assert.equal((s.body.match(/^```/gm)||[]).length%2,0,`${n.title}: ${s.title} unbalanced code`);assert.ok(!/\{\{\s*\w+\(/.test(s.body),`${n.title} unconverted macro`);}
assert.equal(manifest.handbook.topics.length,11);for(const topic of manifest.handbook.topics){for(const id of topic.lessonIds||topic.lessons||[])assert.ok(ids.has(id));}
assert.equal(course.finalQuiz.questions.length,18);assert.ok(course.sections.at(-1).collapsed);console.log('Content validated: 383 checksum-verified sources, 377 HTTP pages, embedded parity, slide limits, code fences, quizzes.');
