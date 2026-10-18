// Flat atmospheric system: lagging haze, hidden image fragments, grain, dust + cracks. All CSS/SVG, one rAF loop.
import { useEffect } from 'react'
import { P, reduced, touch } from './pointer.js'

export default function Atmosphere() {
  useEffect(() => {
    const r = document.documentElement.style
    let hx = innerWidth * 0.6, hy = innerHeight * 0.4, gx = hx, gy = hy, t0 = performance.now(), raf
    const ghosts = () => [...document.querySelectorAll('.ghost')]
    const loop = (now) => {
      const t = (now - t0) / 1000
      const idle = touch || !P.inside
      const tx = idle ? innerWidth * (0.55 + 0.25 * Math.sin(t * 0.17)) : P.x
      const ty = idle ? innerHeight * (0.42 + 0.22 * Math.cos(t * 0.13)) + (touch ? 0 : 0) : P.y
      hx += (tx - hx) * 0.04; hy += (ty - hy) * 0.04      // slow follower
      gx += (tx - gx) * 0.012; gy += (ty - gy) * 0.012    // slower amber follower
      r.setProperty('--hx', hx.toFixed(1) + 'px'); r.setProperty('--hy', hy.toFixed(1) + 'px')
      r.setProperty('--gx', gx.toFixed(1) + 'px'); r.setProperty('--gy', gy.toFixed(1) + 'px')
      r.setProperty('--hp', Math.min(1, P.sy / innerHeight).toFixed(3))
      r.setProperty('--drift', (-Math.min(P.sy * 0.05, 90)).toFixed(1) + 'px')
      ghosts().forEach((g) => { const b = g.parentElement.getBoundingClientRect(); g.style.transform = `translate3d(0,${(b.top * 0.2).toFixed(1)}px,0)` })
      raf = requestAnimationFrame(loop)
    }
    if (!reduced) raf = requestAnimationFrame(loop)
    else { r.setProperty('--hx', '65vw'); r.setProperty('--hy', '40vh'); r.setProperty('--gx', '40vw'); r.setProperty('--gy', '70vh') }
    return () => cancelAnimationFrame(raf)
  }, [])
  return (
    <>
      <svg width="0" height="0" style={{ position: 'absolute' }} aria-hidden="true" focusable="false">
        <defs>
          <filter id="ink" x="-3%" y="-3%" width="106%" height="106%">
            <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3" result="n" />
            <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -6 4.7" result="speck" />
            <feComposite in="SourceGraphic" in2="speck" operator="in" result="worn" />
            <feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="2" seed="8" result="w" />
            <feDisplacementMap in="worn" in2="w" scale="4" />
          </filter>
          <filter id="edge" x="-4%" y="-4%" width="108%" height="108%">
            <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" seed="5" result="w" />
            <feDisplacementMap in="SourceGraphic" in2="w" scale="7" />
          </filter>
        </defs>
      </svg>
      <div className="haze" aria-hidden="true">
        <div className="haze-base" />
        <div className="follow" /><div className="follow amber" />
        <div className="frag"><img src="./img/frag-a.jpg" alt="" /><img src="./img/frag-b.jpg" alt="" /></div>
      </div>
      <svg className="dust" aria-hidden="true" viewBox="0 0 1000 1000" preserveAspectRatio="none" focusable="false">
        <g fill="none" stroke="#f3e9cf" strokeLinecap="round">
          <path d="M493 0 L497 160 L489 290 L495 420 L491 560 L498 730 L494 1000" strokeWidth=".9" opacity=".5" />
          <path d="M0 412 L170 408 L330 415 L420 410" strokeWidth=".8" opacity=".4" />
          <path d="M1000 338 L860 342 L770 336" strokeWidth=".6" opacity=".3" />
          <path d="M210 640 q18 -20 40 -6 t30 -26" strokeWidth=".7" opacity=".35" />
          <path d="M880 880 q-30 -10 -46 14 t-38 8" strokeWidth=".7" opacity=".3" />
        </g>
        <g fill="#f3e9cf" opacity=".4">{[[120,80],[330,230],[640,120],[880,300],[760,610],[90,760],[430,900],[950,720],[560,480],[250,500]].map(([x,y],i)=><circle key={i} cx={x} cy={y} r={i%3?.9:1.6}/>)}</g>
      </svg>
      <div className="grain" aria-hidden="true" />
    </>
  )
}
