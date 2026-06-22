// DPM Learning Hub — shared interactions
document.addEventListener('click', e => {
  // copy-to-clipboard
  const c = e.target.closest('.copy');
  if (c) {
    const code = c.parentElement.querySelector('.code-text') || c.parentElement;
    const txt = (code.dataset.copy || code.textContent).replace(/\s*Copy\s*$/,'').trim();
    navigator.clipboard.writeText(txt).then(()=>{
      const old=c.textContent; c.textContent='Copied'; c.classList.add('done');
      setTimeout(()=>{c.textContent=old; c.classList.remove('done');},1400);
    });
  }
});

// tier tabs
document.querySelectorAll('[data-tiers]').forEach(group=>{
  const btns=group.querySelectorAll('.tier-btn');
  const panels=document.querySelectorAll('[data-tier-panel="'+group.dataset.tiers+'"]');
  btns.forEach(b=>b.addEventListener('click',()=>{
    btns.forEach(x=>x.setAttribute('aria-selected','false'));
    b.setAttribute('aria-selected','true');
    panels.forEach(p=>p.classList.toggle('active', p.dataset.tier===b.dataset.tier));
  }));
});

// quiz
document.querySelectorAll('.quiz').forEach(q=>{
  const opts=q.querySelectorAll('.opt'); const fb=q.querySelector('.fb');
  opts.forEach(o=>o.addEventListener('click',()=>{
    if(q.dataset.done) return;
    q.dataset.done='1';
    opts.forEach(x=>{
      if(x.dataset.correct==='1') x.classList.add('correct');
      else if(x===o) x.classList.add('wrong');
      x.style.cursor='default';
    });
    if(fb){fb.classList.add('show');
      fb.textContent=(o.dataset.correct==='1'?'✓ Correct. ':'✗ Not quite. ')+(fb.dataset.msg||'');}
  }));
});

// mobile menu
const mb=document.querySelector('.menu-btn');
if(mb) mb.addEventListener('click',()=>document.querySelector('.nav-links').classList.toggle('open'));

// scroll progress
const bar=document.querySelector('.scrollbar');
if(bar) addEventListener('scroll',()=>{
  const h=document.documentElement; const p=h.scrollTop/(h.scrollHeight-h.clientHeight);
  bar.style.width=(p*100)+'%';
},{passive:true});
