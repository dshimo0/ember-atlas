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
    const [registryRef,replayRef]=await Promise.all([fetch('/data/regions.json').then(r=>r.json()),fetch('/data/replay-evaluation.json').then(r=>r.json())]);
    const [summary,validation,geography,diagnostics,registry,replayEvaluation]=await Promise.all([verifiedJSON(pointer),verifiedJSON(pointer.validation),fetch('/assets/local-geography.json').then(r=>r.json()),fetch('/data/diagnostics.json').then(r=>r.json()),verifiedJSON(registryRef),verifiedJSON(replayRef)]);
    if(summary.snapshot.sha256!==pointer.snapshot.sha256)throw new Error('Release index mismatch');
    return {pointer,summary,validation,geography,diagnostics,registry,replayEvaluation,registryRef,replayRef};
  })();
  return releasePromise;
}

const datasets=new Map();
export async function loadDataset(region,mode){const release=await loadRelease(),r=release.registry.regions.find(r=>r.id===region);if(!r?.datasets[mode])throw new Error('Regional dataset unavailable');const ref=r.datasets[mode];if(!datasets.has(ref.file))datasets.set(ref.file,verifiedJSON(ref).catch(error=>{datasets.delete(ref.file);throw error;}));const summary=await datasets.get(ref.file);if(summary.region!==region||summary.processing_class!==mode.toUpperCase())throw new Error('Regional scope mismatch');return summary;}
