/* Loopback-only HTTP teaching fixtures; no dependencies or persistent writes. */
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
function createPracticeServer(){return http.createServer(async(req,res)=>{
  const u=new URL(req.url,'http://localhost'),route=u.pathname;
  const send=(status,body='',headers={})=>{const data=Buffer.from(body);res.writeHead(status,{'Content-Length':data.length,...headers});res.end(req.method==='HEAD'?undefined:data);};
  const json=(status,value,headers={})=>send(status,JSON.stringify(value),{'Content-Type':'application/json; charset=utf-8',...headers});
  try{
    if(route==='/lessons'){
      if(req.method==='POST'){
        if(!/^application\/json(?:;|$)/i.test(req.headers['content-type']||''))return json(415,{error:'Send application/json'});
        let body='';for await(const chunk of req){body+=chunk;if(Buffer.byteLength(body)>16384)return json(413,{error:'Body too large'});}
        let value;try{value=JSON.parse(body);}catch{return json(400,{error:'Invalid JSON'});}
        if(!value||typeof value.title!=='string'||!value.title.trim())return json(422,{error:'A nonempty title is required'});
        return json(201,{id:'practice',title:value.title},{Location:'/lessons/practice'});
      }
      if(!['GET','HEAD'].includes(req.method))return json(405,{error:'Method not allowed'},{Allow:'GET, HEAD, POST'});
      return json(200,{lessons:[{id:'syntax',title:'HTTP messages'}]},{'Cache-Control':'no-store'});
    }
    if(!['GET','HEAD'].includes(req.method))return json(405,{error:'Method not allowed'},{Allow:'GET, HEAD'});
    if(route==='/missing')return json(404,{error:'No such resource'});
    if(route==='/empty'){res.writeHead(204);return res.end();}
    if(route==='/invalid-json')return send(200,'{"broken":',{'Content-Type':'application/json'});
    if(route==='/redirect')return send(303,'',{Location:'/lessons'});
    if(route==='/etag'){
      const headers={ETag:'"lesson-v1"','Cache-Control':'private, max-age=0'};
      if(req.headers['if-none-match']==='"lesson-v1"'){res.writeHead(304,headers);return res.end();}
      return json(200,{title:'HTTP messages'},headers);
    }
    if(route==='/slow'){return setTimeout(()=>{if(!res.destroyed)json(200,{message:'Slow response'});},750);}
    const filename=path.resolve(root,'.'+decodeURIComponent(route==='/'?'/index.html':route));
    if(!filename.startsWith(root+path.sep)||!fs.existsSync(filename)||!fs.statSync(filename).isFile())return json(404,{error:'No such file'});
    const ext=path.extname(filename),mime={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json','.md':'text/plain; charset=utf-8'}[ext]||'application/octet-stream';
    send(200,fs.readFileSync(filename),{'Content-Type':mime});
  }catch{if(!res.headersSent)json(400,{error:'Invalid request'});else res.end();}
});}
module.exports={createPracticeServer};
if(require.main===module){const port=Number(process.env.PORT||8000);if(!Number.isInteger(port)||port<1||port>65535)throw Error('Invalid PORT');createPracticeServer().listen(port,'127.0.0.1',()=>console.log(`HTTP LMS: http://localhost:${port} (Ctrl+C to stop)`));}
