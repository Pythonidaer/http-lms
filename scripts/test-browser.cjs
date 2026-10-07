const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright'),{createPracticeServer}=require('./practice-server.cjs');
(async()=>{
 const server=createPracticeServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}`;
 let browser;try{
  assert.equal((await fetch(base+'/missing')).status,404);assert.equal((await fetch(base+'/empty')).status,204);await assert.rejects((await fetch(base+'/invalid-json')).json());
  assert.equal((await fetch(base+'/redirect',{redirect:'manual'})).status,303);assert.equal((await fetch(base+'/redirect')).status,200);
  const etag=await fetch(base+'/etag');assert.equal(etag.headers.get('etag'),'"lesson-v1"');assert.equal((await fetch(base+'/etag',{headers:{'If-None-Match':etag.headers.get('etag')}})).status,304);
  assert.equal((await fetch(base+'/lessons',{method:'HEAD'})).headers.get('content-type'),'application/json; charset=utf-8');
  assert.equal((await fetch(base+'/lessons',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:'Practice'})})).status,201);
  assert.equal((await fetch(base+'/lessons',{method:'POST',headers:{'Content-Type':'application/json'},body:'{'})).status,400);
  await assert.rejects(fetch(base+'/slow',{signal:AbortSignal.timeout(50)}));
  const opts={headless:true};if(process.env.CHROMIUM_PATH){opts.executablePath=process.env.CHROMIUM_PATH;if(process.env.CHROMIUM_ARGS_MODULE)opts.args=(await import(process.env.CHROMIUM_ARGS_MODULE)).default.args;}
  browser=await chromium.launch(opts);
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const width of [390,768,1440]){await page.setViewportSize({width,height:950});await page.goto(base);await page.waitForSelector('#lms-heading');assert.equal(await page.locator('#lms-heading').textContent(),'Goal and sources');assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   if(width===390){await page.locator('.lms-menu-button').click();assert.equal(await page.locator('#lms-nav').getAttribute('aria-hidden'),'false');await page.keyboard.press('Escape');assert.equal(await page.locator('#lms-nav').getAttribute('aria-hidden'),'true');await page.locator('[data-lms="outline"]').click();}
   assert.equal(await page.locator('[data-lms-section="reference-library"]').getAttribute('open'),null);
   await page.locator('#lms-search').fill('Cache-Control');assert.ok((await page.locator('.lms-search-status').textContent()).includes('matching'));
   assert.equal(await page.locator('[data-lms-section="reference-library"]').getAttribute('open'),'');
   await page.locator('#lms-search').fill('zzNoMatch0123');assert.equal(await page.locator('.lms-search-status').textContent(),'No matching lessons');
   await page.locator('#lms-search').fill('');assert.equal(await page.locator('[data-lms-section="reference-library"]').getAttribute('open'),null);
   if(process.env.LMS_TEST_ARTIFACTS){fs.mkdirSync(process.env.LMS_TEST_ARTIFACTS,{recursive:true});await page.screenshot({path:path.join(process.env.LMS_TEST_ARTIFACTS,`http-${width}.png`),fullPage:true});}
  }
  // Gating fixture: completed core lessons, unopened optional references.
  await page.evaluate(()=>{const raw=JSON.parse(document.querySelector('#lms-course-data').textContent),course=LMS.validate(raw),records={};for(const n of LMS.flatten(course.sections)){if(n.optional)continue;let hash=0;for(const ch of JSON.stringify(n))hash=(Math.imul(31,hash)+ch.charCodeAt(0))|0;records[n.id]={fingerprint:String(hash),completed:true,seconds:0,slideSeen:[],attempts:[]};}localStorage.setItem('design-lab-lms-progress-'+course.id,JSON.stringify({records,unlockAll:false}));});
  await page.reload();await page.locator('[data-id="http-final"]').click();assert.equal(await page.locator('#lms-heading').textContent(),'Final assessment — HTTP skills');
  const questions=JSON.parse(fs.readFileSync('course.json')).finalQuiz.questions;for(const q of questions)await page.locator(`input[name="q-${q.id}"][value="${q.answer}"]`).check();await page.locator('#lms-quiz button[type="submit"]').click();assert.ok((await page.locator('.lms-result').last().textContent()).includes('100%'));
  await page.locator('[aria-label="Reports"]').click();assert.ok((await page.locator('main').textContent()).includes('100'));
  const unsafe=await page.evaluate(()=>{const d=document.createElement('div');d.innerHTML=LMSMarkdown('<script>alert(1)</script>\n\n[x](javascript:alert(1))\n\n<img src=x onerror=alert(1)>');return d.querySelector('script,[onerror],a[href^="javascript:"]')!==null;});assert.equal(unsafe,false);assert.deepEqual(errors,[]);
  console.log('Browser passed: fixtures, 390/768/1440 widths, mobile menu, search/collapse, optional reference gating, final quiz/report, inert source HTML.');
 }finally{await browser?.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;});
