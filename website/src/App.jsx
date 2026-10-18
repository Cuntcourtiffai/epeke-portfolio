import { useEffect, useState } from 'react'
import C from './content.json'
import Atmosphere from './Atmosphere.jsx'
import Flower from './Flower.jsx'
import { reduced } from './pointer.js'

// Three stacked copies of one word: ivory (readable) + pink + gold. They sit exactly on top of each other
// until the print "slips out of register" (hover, tap, or once after load), then settle back.
const Word = ({ t, cls }) => (
  <span className={`w ${cls}`} aria-hidden="true">
    <span className="l pink">{t}</span><span className="l gold">{t}</span><span className="l ivory">{t}</span><span className="l tint">{t}</span>
  </span>
)

function Card({ p }) {
  return (
    <article className="card" data-cat={p.cat}>
      <div className="frame"><video controls playsInline preload="none" poster={`./posters/${p.id}.jpg`} src={`./videos/${p.id}.mp4`} aria-label={p.title} /></div>
      <div className="card-meta">
        <span className="tag">{p.cat}</span>
        <h3>{p.title}</h3>
        <p>{p.desc}</p>
        <small>Creator concept video · {p.subject}</small>
        {p.url && <a href={p.url} target="_blank" rel="noopener noreferrer">View original ↗</a>}
      </div>
    </article>
  )
}

export default function App() {
  const cats = ['All', ...Array.from(new Set(C.projects.map((p) => p.cat)))]
  const [f, setF] = useState('All')
  const [slip, setSlip] = useState(false)
  const slipNow = () => { if (reduced || slip) return; setSlip(true); setTimeout(() => setSlip(false), 2400) }
  useEffect(() => { const t = setTimeout(slipNow, 3200); return () => clearTimeout(t) }, [])
  const list = C.projects.filter((p) => f === 'All' || p.cat === f)
  return (
    <>
      <Atmosphere />
      <a className="skip" href="#work">Skip to work</a>
      <header className="nav">
        <a href="#top" className="brand">E. Vuyisani</a>
        <nav aria-label="Primary"><a href="#work">Work</a><a href="#about">About</a><a href="#services">Services</a><a href="#process">Process</a><a href="#contact">Contact</a></nav>
      </header>
      <main id="top">
        <section className="hero">
          <div className="hero-top cap"><span>UGC Creator</span><span>Beauty</span><span>Fashion</span><span>Lifestyle</span></div>
          <h1 aria-label={C.name} className={slip ? 'slip' : ''} onPointerEnter={slipNow} onClick={slipNow}>
            <Word t="Epeke" cls="w1" /><Word t="Vuyisani" cls="w2" />
          </h1>
          <Flower />
          <div className="hero-mid">
            <p className="tagline">{C.tagline}</p>
            <div className="ctas"><a className="btn gold" href="#work">View My Work</a><a className="btn" href="#contact">Work With Me</a></div>
          </div>
          <div className="hero-bot cap"><span>Real faces</span><span>soft light</span><span>content</span><span>that feels like taste</span></div>
        </section>

        <section id="work" className="sec">
          <div className="ghost" aria-hidden="true">Work</div>
          <p className="cap">01 — Selected work</p><h2>Creator-made <em>concept films</em></h2>
          <div className="chips" role="group" aria-label="Filter by category">
            {cats.map((c) => <button key={c} className={c === f ? 'on' : ''} aria-pressed={c === f} onClick={() => setF(c)}>{c}</button>)}
          </div>
          <div className="grid">{list.map((p) => <Card key={p.id} p={p} />)}</div>
        </section>

        <section id="about" className="sec about">
          <div className="portrait"><img src="./img/portrait.jpg" alt="Portrait of Epeke Vuyisani" loading="lazy" /></div>
          <div><p className="cap">02 — About</p><h2>Taste, light, <em>honest product</em></h2><p className="lead">{C.about}</p>
            <ul className="pills">{C.niches.map((n) => <li key={n}>{n}</li>)}</ul></div>
        </section>

        <section id="services" className="sec">
          <p className="cap">03 — Services</p><h2>What I can make <em>for you</em></h2>
          <ul className="svc">{C.services.map(([t, d]) => <li key={t}><h3>{t}</h3><p>{d}</p></li>)}</ul>
          <a className="btn gold" href={`mailto:${C.email}?subject=Quote%20request`}>Request a Quote</a>
        </section>

        <section id="process" className="sec">
          <p className="cap">04 — Creative process</p><h2>Four steps, <em>no guesswork</em></h2>
          <ol className="steps">{C.process.map(([n, t, d]) => <li key={n}><span>{n}</span><h3>{t}</h3><p>{d}</p></li>)}</ol>
        </section>

        <section id="contact" className="sec contact">
          <div className="ghost" aria-hidden="true">Hello</div>
          <p className="cap">05 — Contact</p><h2>Let’s make <em>something real</em></h2>
          <ul className="links">
            <li><span>Email</span><a href={`mailto:${C.email}`}>{C.email}</a></li>
            <li><span>Instagram</span><a href={C.instagram} target="_blank" rel="noopener noreferrer">{C.instagramHandle}</a></li>
            <li><span>TikTok</span><a href={C.tiktok} target="_blank" rel="noopener noreferrer">{C.tiktokHandle}</a></li>
            <li><span>WhatsApp</span><a href={C.whatsapp} target="_blank" rel="noopener noreferrer">{C.whatsappDisplay}</a></li>
          </ul>
          <a className="btn gold" href={`mailto:${C.email}?subject=Quote%20request`}>Request a Quote</a>
        </section>
      </main>
      <footer><span>© 2026 Epeke Vuyisani</span><span>Creator concept films shown as portfolio work.</span></footer>
    </>
  )
}
