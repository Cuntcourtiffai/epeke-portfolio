// Flat halftone flower on a 2D canvas. Effects: A) dots drift away from the pointer and slowly return,
// D) the offset shadow moves against the pointer, E) the image dissolves and reassembles (load, tap, re-entry).
import { useEffect, useRef } from 'react'
import data from './halftone.json'
import { P, reduced, touch } from './pointer.js'

const COLORS = ['#7d5217', '#9d6f22', '#c0922f', '#dcb24a', '#f0cb66', '#ffe48a']
export default function Flower() {
  const wrap = useRef(), cv = useRef(), img = useRef()
  useEffect(() => {
    const c = cv.current, ctx = c.getContext('2d'), N = data.dots.length, MAXR = data.sp * 0.66
    const hx = new Float32Array(N), hy = new Float32Array(N), x = new Float32Array(N), y = new Float32Array(N)
    const vx = new Float32Array(N), vy = new Float32Array(N), r = new Float32Array(N), a = new Float32Array(N), bk = new Uint8Array(N)
    data.dots.forEach(([X, Y, R], i) => { hx[i] = x[i] = X; hy[i] = y[i] = Y; r[i] = R; a[i] = 1; bk[i] = Math.min(5, Math.floor(Math.pow(R / MAXR, 1.4) * 6)) })
    let last = 0, scale = 1, raf = 0, visible = false, seen = false, sox = 9, soy = 13, svx = 0, svy = 0
    const resize = () => { const b = c.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 2); c.width = Math.max(1, b.width * d); c.height = Math.max(1, b.height * d); scale = c.width / data.w; if (!raf) draw() }
    const shatter = (k = 1) => { for (let i = 0; i < N; i++) { const th = Math.random() * 6.283, s = (4 + Math.random() * 9) * k; vx[i] += Math.cos(th) * s; vy[i] += Math.sin(th) * s; a[i] = 0.55 } }
    const draw = () => {
      ctx.clearRect(0, 0, c.width, c.height)
      ctx.fillStyle = 'rgba(105,48,8,.42)'; ctx.beginPath()                      // wrong shadow: flat offset duplicate
      for (let i = 0; i < N; i += 1) { const rr = r[i] * a[i] * 1.12; if (rr < .4) continue; const X = (x[i] + sox) * scale, Y = (y[i] + soy) * scale; ctx.moveTo(X + rr * scale, Y); ctx.arc(X, Y, rr * scale, 0, 6.283) }
      ctx.fill()
      for (let b = 0; b < 6; b++) { ctx.fillStyle = COLORS[b]; ctx.beginPath()
        for (let i = 0; i < N; i++) { if (bk[i] !== b) continue; const rr = r[i] * a[i]; if (rr < .4) continue; const X = x[i] * scale, Y = y[i] * scale; ctx.moveTo(X + rr * scale, Y); ctx.arc(X, Y, rr * scale, 0, 6.283) }
        ctx.fill() }
    }
    const step = (now) => {
      const k2 = Math.min(4, Math.max(0.5, (now - (last || now - 16.7)) / 16.7)); last = now; const damp = Math.pow(0.93, k2)
      const bb = c.getBoundingClientRect(), k = data.w / bb.width, px = (P.x - bb.left) * k, py = (P.y - bb.top) * k, R = 170, R2 = R * R
      const on = P.inside && !touch
      for (let i = 0; i < N; i++) {
        let near = false
        if (on) { const dx = x[i] - px, dy = y[i] - py, d2 = dx * dx + dy * dy
          if (d2 < R2 && d2 > 1) { const d = Math.sqrt(d2), f = (1 - d / R) ** 2; vx[i] += (dx / d) * f * 2.6 - (dy / d) * f * 0.7; vy[i] += (dy / d) * f * 2.6 + (dx / d) * f * 0.7; near = true } }
        vx[i] += (hx[i] - x[i]) * 0.0055 * k2; vy[i] += (hy[i] - y[i]) * 0.0055 * k2; vx[i] *= damp; vy[i] *= damp; x[i] += vx[i] * k2; y[i] += vy[i] * k2
        a[i] += ((near ? 0.1 : 1) - a[i]) * Math.min(1, (near ? 0.18 : 0.02) * k2)
      }
      svx += (P.vx - svx) * 0.2; svy += (P.vy - svy) * 0.2; P.vx *= 0.8; P.vy *= 0.8       // shadow answers with a perpendicular, delayed push
      const tx = 9 - svy * 1.1, ty = 13 + svx * 1.1
      sox += (Math.max(-46, Math.min(46, tx)) - sox) * 0.05; soy += (Math.max(-46, Math.min(46, ty)) - soy) * 0.05
      draw(); raf = visible ? requestAnimationFrame(step) : 0
    }
    const start = () => { if (!raf && !reduced) raf = requestAnimationFrame(step) }
    resize(); img.current.style.opacity = 0
    const ro = new ResizeObserver(resize); ro.observe(c)
    const io = new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) { if (seen) shatter(0.45); seen = true; start() } }, { threshold: 0.15 }); io.observe(c)
    if (!reduced) { shatter(2.8); for (let i = 0; i < N; i++) { x[i] += (Math.random() - .5) * 700; y[i] += (Math.random() - .5) * 700; a[i] = 0 } }
    const tap = (e) => { const b = wrap.current.parentElement.getBoundingClientRect(); if (e.clientY >= b.top && e.clientY <= b.bottom && (touch || e.target.closest?.('.hero'))) shatter(0.9) }
    addEventListener('pointerdown', tap)
    return () => { cancelAnimationFrame(raf); ro.disconnect(); io.disconnect(); removeEventListener('pointerdown', tap) }
  }, [])
  return (
    <div className="flower" ref={wrap} aria-hidden="true">
      <img ref={img} src="./img/halftone-flower.png" alt="" width="1000" height="1250" />
      <canvas ref={cv} />
    </div>
  )
}
