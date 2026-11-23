const {chromium}=require('playwright');
const L={tendo:[1080,1080],muscul:[1080,1080],molla:[1080,900],donut:[1080,800],paret:[1080,1080],esquat:[1080,1080],salt:[1080,1080]};
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
for (const s of (process.argv[2]||Object.keys(L).join(',')).split(',')){const [w,h]=L[s];
 const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>console.log(s,e.message));
 await p.goto(`http://localhost:8765/scene.html?s=${s}&w=${w}&h=${h}`);await p.waitForFunction('window.done',null,{timeout:120000});
 await p.locator('#c').screenshot({path:`r_${s}.png`,omitBackground:true});await p.close();console.log('ok',s);}
await b.close();})();
