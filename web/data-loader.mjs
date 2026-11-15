let releasePromise;
export async function sha256(bytes) {
  const hash=await crypto.subtle.digest('SHA-256',bytes);
  return [...new Uint8Array(hash)].map(v=>v.toString(16).padStart(2,'0')).join('');
}
export async function verifiedJSON(ref,compressed=false) {
  const response=await fetch('/data/'+ref.file);
  if(!response.ok)throw new Error('Data file unavailable');
  const bytes=compressed?await new Response(response.body.pipeThrough(new DecompressionStream('gzip'))).arrayBuffer():await response.arrayBuffer();
  if(await sha256(bytes)!==ref.sha256)throw new Error('Data integrity check failed');
  return JSON.parse(new TextDecoder().decode(bytes));
}
export function loadRelease() {
  if(!releasePromise)releasePromise=(async()=>{
    const pointer=await(await fetch('/data/dashboard.json')).json();
    const [summary,validation,geography,diagnostics]=await Promise.all([verifiedJSON(pointer),verifiedJSON(pointer.validation),fetch('/assets/local-geography.json').then(r=>r.json()),fetch('/data/diagnostics.json').then(r=>r.json())]);
    if(summary.snapshot.sha256!==pointer.snapshot.sha256)throw new Error('Release index mismatch');
    return {pointer,summary,validation,geography,diagnostics};
  })();
  return releasePromise;
}
