const {chromium}=require('playwright');
const L={aquil:[875,1000],muscul:[875,1000],molla:[875,1000],paret:[750,1000],esquat:[750,1000],salt:[750,1000]};
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
for (const s of (process.argv[2]||Object.keys(L).join(',')).split(',')){const [w,h]=L[s];const pr=+(process.argv[3]||2);
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:pr});p.on('pageerror',e=>console.log(s,e.message));p.on('console',m=>{if(m.type()==='error')console.log(s,m.text())});
 const t=Date.now();await p.goto(`http://localhost:8765/scene2.html?s=${s}&w=${w}&h=${h}&pr=${pr}`);await p.waitForFunction('window.done',null,{timeout:600000});
 await p.locator('#c').screenshot({path:`q_${s}.png`});await p.close();console.log('ok',s,(Date.now()-t)/1000+'s');}
await b.close();})();
