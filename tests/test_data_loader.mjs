import test from 'node:test';
import assert from 'node:assert/strict';
import {verifiedJSON,sha256} from '../web/data-loader.mjs';
test('pinned public data requires exact repository, full commit and verified content',async()=>{
 const oldFetch=globalThis.fetch;const bytes=new TextEncoder().encode('{"ok":true}');const digest=await sha256(bytes);let requested;
 globalThis.fetch=async url=>{requested=url;return new Response(bytes)};
 try{
  const url='https://raw.githubusercontent.com/dshimo0/ember-atlas/'+'a'.repeat(40)+'/web/data/example.json';
  assert.deepEqual(await verifiedJSON({url,sha256:digest}),{ok:true});assert.equal(requested,url);
  for(const bad of [url.replace('dshimo0','other'),url.replace('a'.repeat(40),'work'),url+'?key=secret',url.replace('https:','http:')])await assert.rejects(verifiedJSON({url:bad,sha256:digest}),/Invalid pinned/);
  await assert.rejects(verifiedJSON({url,sha256:'0'.repeat(64)}),/integrity/);
 }finally{globalThis.fetch=oldFetch;}
});
