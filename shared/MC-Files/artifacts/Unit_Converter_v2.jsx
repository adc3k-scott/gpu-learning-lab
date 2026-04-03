'use client';
import { useState } from 'react';
const CONVERSIONS = [
  {from:'mph',to:'km/h',factor:1.60934,label:'MPH → KM/H'},
  {from:'km/h',to:'mph',factor:0.621371,label:'KM/H → MPH'},
  {from:'miles',to:'km',factor:1.60934,label:'Miles → KM'},
  {from:'km',to:'miles',factor:0.621371,label:'KM → Miles'},
  {from:'gallons',to:'liters',factor:3.78541,label:'Gallons → Liters'},
  {from:'liters',to:'gallons',factor:0.264172,label:'Liters → Gallons'},
  {from:'ft-lbs',to:'Nm',factor:1.35582,label:'Ft-lbs → Nm'},
  {from:'Nm',to:'ft-lbs',factor:0.737562,label:'Nm → Ft-lbs'},
  {from:'PSI',to:'bar',factor:0.0689476,label:'PSI → Bar'},
  {from:'bar',to:'PSI',factor:14.5038,label:'Bar → PSI'},
  {from:'in',to:'mm',factor:25.4,label:'Inches → MM'},
  {from:'mm',to:'in',factor:0.0393701,label:'MM → Inches'},
];
export default function UnitConverter() {
  const [value, setValue] = useState('');
  const [selected, setSelected] = useState(0);
  const conv = CONVERSIONS[selected];
  const result = value ? (parseFloat(value) * conv.factor).toFixed(4) : '';
  return (<div className="min-h-screen bg-background">
    <header className="border-b border-border px-4 py-3"><div className="max-w-4xl mx-auto flex items-center gap-3"><a href="/tools" className="text-text-muted hover:text-text-primary text-sm">← Tools</a><span className="text-border">|</span><h1 className="font-bold">🔄 Unit Converter</h1></div></header>
    <div className="max-w-lg mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-2">Unit Converter</h2><p className="text-text-muted text-sm mb-8">Convert between common vehicle measurement units.</p>
      <div className="flex flex-wrap gap-2 mb-6">{CONVERSIONS.map((c,i)=>(<button key={i} onClick={()=>setSelected(i)} className={`px-3 py-1.5 rounded-full text-xs font-medium ${selected===i?'bg-harley text-white':'bg-surface text-text-muted border border-border'}`}>{c.label}</button>))}</div>
      <div className="mc-card p-6">
        <div className="mb-4"><label className="block text-sm font-medium mb-1.5">{conv.from}</label><input type="number" value={value} onChange={e=>setValue(e.target.value)} placeholder="Enter value" className="mc-input text-2xl"/></div>
        <div className="text-center text-2xl text-text-muted my-4">↓</div>
        <div><label className="block text-sm font-medium mb-1.5">{conv.to}</label><div className="mc-input text-2xl bg-background font-bold" style={{color:'#E8720E'}}>{result||'—'}</div></div>
      </div>
    </div></div>);
}
