// Shared, throttled pointer + scroll state. Effects read this inside requestAnimationFrame loops.
export const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches
export const touch = !matchMedia('(pointer: fine)').matches
export const P = { x: -9999, y: -9999, vx: 0, vy: 0, sy: 0, inside: false }
if (!touch && !reduced) {
  addEventListener('pointermove', (e) => { if (P.inside) { P.vx += e.clientX - P.x; P.vy += e.clientY - P.y } P.x = e.clientX; P.y = e.clientY; P.inside = true }, { passive: true })
  document.documentElement.addEventListener('mouseleave', () => { P.inside = false; P.x = P.y = -9999 })
}
addEventListener('scroll', () => { P.sy = scrollY }, { passive: true })
