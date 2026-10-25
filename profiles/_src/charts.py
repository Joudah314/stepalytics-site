"""Charts for "study" project pages, drawn from the numbers in projects/<slug>.toml (no images, no JavaScript).

    ladder   the error of each approach, as horizontal bars (HTML, so the text stays sharp on any screen)
    recruit  people to recruit for 200 completes against the qualification rate (inline SVG, wide and narrow)
    flow     the steps of the method as boxes and arrows (inline SVG, wide and narrow; the site's diagram style)

Every chart is a <figure> with a caption; the SVGs carry a title and description for screen readers.
"""
from __future__ import annotations

import html
import math

esc = html.escape


def _num(v) -> str:
    return f"{v:,.0f}" if abs(v) >= 1000 else f"{v:g}"


def ladder(rows: list[dict], caption: str, table_label: str) -> str:
    top = math.ceil(max(r["value"] for r in rows) / 5) * 5
    items = []
    for r in rows:
        width = r["value"] / top * 100
        note = f' <span class="ladder-note">{esc(r["note"])}</span>' if r.get("note") else ""
        items.append(
            f'<li class="ladder-row{" best" if r.get("best") else ""}"><span class="ladder-label">{esc(r["label"])}</span>'
            f'<span class="ladder-track"><span class="ladder-bar" style="width:{width:.1f}%"></span>'
            f'<span class="ladder-val">{_num(r["value"])}{note}</span></span></li>')
    table = "".join(f"<tr><th scope=\"row\">{esc(r['label'])}</th><td>{_num(r['value'])}</td></tr>" for r in rows)
    return (f'<figure class="chart ladder"><ol class="ladder-rows">{"".join(items)}</ol>'
            f'<figcaption>{esc(caption)}</figcaption>'
            f'<details class="chart-data"><summary>{esc(table_label)}</summary><table><tbody>{table}</tbody></table></details>'
            f'</figure>')


def _recruit_svg(cls: str, w: int, h: int, font: int, title: str, desc: str, tag: str) -> str:
    left, right, top, bottom = (font * 4, font * 2, 16, font * 3)
    pw, ph = w - left - right, h - top - bottom
    x = lambda rate: left + rate / 100 * pw  # noqa: E731  rate in %
    y = lambda n: top + ph - n / 4000 * ph  # noqa: E731  people
    need = lambda rate: 200 / (rate / 100)  # noqa: E731
    pts = " ".join(f"{x(r):.1f},{y(need(r)):.1f}" for r in [5 + i * 0.5 for i in range(191)])
    parts = [f'<svg class="ch {cls}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{tag}-t {tag}-d">'
             f'<title id="{tag}-t">{esc(title)}</title><desc id="{tag}-d">{esc(desc)}</desc>']
    for n in (0, 1000, 2000, 3000, 4000):
        parts.append(f'<line class="ch-grid" x1="{left}" x2="{w - right}" y1="{y(n):.1f}" y2="{y(n):.1f}"/>'
                     f'<text class="ch-lab ch-y" x="{left - 6}" y="{y(n):.1f}" font-size="{font}">{n:,}</text>')
    for r in (5, 20, 40, 60, 80, 100):
        parts.append(f'<text class="ch-lab ch-x" x="{x(r):.1f}" y="{top + ph + font + 4}" font-size="{font}">{r}%</text>')
    parts.append(f'<text class="ch-title" x="{left + pw / 2:.1f}" y="{h - 4}" font-size="{font}">Qualification rate</text>'
                 f'<text class="ch-title" x="{font}" y="{top + ph / 2:.1f}" font-size="{font}" '
                 f'transform="rotate(-90 {font} {top + ph / 2:.1f})">People to recruit</text>')
    for rate, label in ((50, "50%: about 350–470"), (20, "20%: about 740–1,540")):
        lo, hi = need(rate + 7), need(rate - 7)
        parts.append(f'<rect class="ch-band" x="{x(rate - 7):.1f}" y="{y(hi):.1f}" width="{x(rate + 7) - x(rate - 7):.1f}" '
                     f'height="{max(y(lo) - y(hi), 3):.1f}"/>')
        parts.append(f'<text class="ch-ann" x="{x(rate + 7) + 6:.1f}" y="{y(hi) - 4:.1f}" font-size="{font}">{label}</text>')
    parts.append(f'<polyline class="ch-line" points="{pts}"/></svg>')
    return "".join(parts)


def recruit(caption: str, title: str, desc: str) -> str:
    return (f'<figure class="chart">{_recruit_svg("ch-wide", 640, 330, 14, title, desc, "rc-w")}'
            f'{_recruit_svg("ch-narrow", 360, 300, 12, title, desc, "rc-n")}'
            f'<figcaption>{esc(caption)}</figcaption></figure>')


def _lines(label: str, cx: float, cy: float) -> str:
    lines = [part.strip() for part in label.split("|") if part.strip()]
    first = -(len(lines) - 1) * 0.6
    spans = "".join(f'<tspan x="{cx:.0f}" dy="{first if i == 0 else 1.2:.1f}em">{esc(t)}</tspan>' for i, t in enumerate(lines))
    return f'<text class="dg-text" x="{cx:.0f}" y="{cy:.0f}">{spans}</text>'


def flow(boxes: list[str], title: str, desc: str) -> str:
    n = len(boxes)
    head = ('<defs><marker id="{m}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-head"/></marker></defs>')
    # wide: one row
    bw, bh, gap = 190, 78, 38
    w = 10 * 2 + n * bw + (n - 1) * gap
    wide = [f'<svg class="dg dg-wide" viewBox="0 0 {w} {bh + 20}" role="img" aria-labelledby="fl-t-w fl-d-w">'
            f'<title id="fl-t-w">{esc(title)}</title><desc id="fl-d-w">{esc(desc)}</desc>', head.format(m="fl-aw")]
    for i, label in enumerate(boxes):
        x0 = 10 + i * (bw + gap)
        last = " dg-human" if i == n - 1 else ""
        wide.append(f'<g class="dg-node"><rect class="dg-box{last}" x="{x0}" y="10" width="{bw}" height="{bh}" rx="6"/>'
                    f'{_lines(label, x0 + bw / 2, 10 + bh / 2)}</g>')
        if i < n - 1:
            wide.append(f'<path class="dg-arrow" d="M{x0 + bw},{10 + bh / 2:.0f} H{x0 + bw + gap - 4}" marker-end="url(#fl-aw)"/>')
    wide.append("</svg>")
    # tall: one column
    tw, th, tgap = 300, 70, 30
    h = 10 * 2 + n * th + (n - 1) * tgap
    tall = [f'<svg class="dg dg-tall" viewBox="0 0 {tw + 20} {h}" role="img" aria-labelledby="fl-t-t fl-d-t">'
            f'<title id="fl-t-t">{esc(title)}</title><desc id="fl-d-t">{esc(desc)}</desc>', head.format(m="fl-at")]
    for i, label in enumerate(boxes):
        y0 = 10 + i * (th + tgap)
        last = " dg-human" if i == n - 1 else ""
        tall.append(f'<g class="dg-node"><rect class="dg-box{last}" x="10" y="{y0}" width="{tw}" height="{th}" rx="6"/>'
                    f'{_lines(label, 10 + tw / 2, y0 + th / 2)}</g>')
        if i < n - 1:
            tall.append(f'<path class="dg-arrow" d="M{10 + tw / 2:.0f},{y0 + th} V{y0 + th + tgap - 4}" marker-end="url(#fl-at)"/>')
    tall.append("</svg>")
    return f'<figure class="diagram">{"".join(wide)}{"".join(tall)}</figure>'



# --- StepAlytics views: built from the project's daily table (projects/data/stepalytics-daily.csv) ------------------
import csv  # noqa: E402
from datetime import date, timedelta  # noqa: E402
from statistics import mean  # noqa: E402

LEVELS = (5000, 10000, 15000, 20000)  # steps: <5k, 5-10k, 10-15k, 15-20k, 20k+


def read_daily(path) -> list[dict]:
    rows = []
    for r in csv.DictReader(open(path, encoding="utf-8")):
        rows.append({"date": date.fromisoformat(r["date"]), "steps": int(r["steps"]),
                     "heavy": r["rain_category"].startswith("Heavy"), "cold": r["temp_category"].startswith("Cold"),
                     "program": r["program_phase"] not in ("Before program", "After program"),
                     "phase": r["program_phase"], "speed": float(r["walking_speed_kmh"]),
                     "cadence": float(r["walking_cadence"])})
    return rows


def _level(steps: int) -> int:
    return sum(steps >= t for t in LEVELS)


def _cal_svg(days: list[dict], weeks_per_block: int, cell: int, cls: str, tag: str, title: str, desc: str) -> str:
    start = days[0]["date"] - timedelta(days=days[0]["date"].weekday())
    n_weeks = (days[-1]["date"] - start).days // 7 + 1
    blocks = math.ceil(n_weeks / weeks_per_block)
    left, top, block_h = 30, 16, 7 * cell + 22
    w = left + weeks_per_block * cell + 4
    h = blocks * block_h + 2
    out = [f'<svg class="cal {cls}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{tag}-t {tag}-d">'
           f'<title id="{tag}-t">{esc(title)}</title><desc id="{tag}-d">{esc(desc)}</desc>']
    for b in range(blocks):
        y0 = b * block_h + top
        for i, name in ((0, "Mon"), (2, "Wed"), (4, "Fri"), (6, "Sun")):
            out.append(f'<text class="cal-lab" x="0" y="{y0 + i * cell + cell - 3}">{name}</text>')
    seen_months = set()
    for d in days:
        k = (d["date"] - start).days
        week, dow = divmod(k, 7)
        b, col = divmod(week, weeks_per_block)
        x, y = left + col * cell, b * block_h + top + dow * cell
        month = (d["date"].year, d["date"].month)
        if month not in seen_months and dow == 0 or (month not in seen_months and d is days[0]):
            seen_months.add(month)
            out.append(f'<text class="cal-lab" x="{x}" y="{b * block_h + top - 4}">{d["date"]:%b}</text>')
        flags = (" wx" if d["heavy"] or d["cold"] else "") + (" pg" if d["program"] else "")
        tip = (f'{d["date"]:%a %d %b %Y}: {d["steps"]:,} steps' + (" · heavy rain" if d["heavy"] else "")
               + (" · cold" if d["cold"] else "") + (" · program" if d["program"] else ""))
        out.append(f'<rect class="cal-day l{_level(d["steps"])}{flags}" x="{x}" y="{y}" width="{cell - 2}" '
                   f'height="{cell - 2}" rx="2"><title>{esc(tip)}</title></rect>')
    out.append("</svg>")
    return "".join(out)


def calendar(days: list[dict], caption: str, modes: list[dict], title: str, desc: str, table_label: str) -> str:
    """A year of days (weeks across, weekdays down), coloured by steps; buttons outline weather or program days."""
    buttons = "".join(f'<button type="button" class="cal-mode" data-mode="{esc(m["id"])}" '
                      f'aria-pressed="{"true" if i == 0 else "false"}">{esc(m["label"])}</button>'
                      for i, m in enumerate(modes))
    legend_labels = ("under 5,000", "5,000–10,000", "10,000–15,000", "15,000–20,000", "20,000+")
    legend = "".join(f'<span class="cal-key"><span class="cal-sw l{i}"></span>{esc(t)}</span>'
                     for i, t in enumerate(legend_labels))
    months = {}
    for d in days:
        months.setdefault(f'{d["date"]:%b %Y}', []).append(d["steps"])
    table = "".join(f"<tr><th scope=\"row\">{m}</th><td>{sorted(v)[len(v) // 2]:,}</td>"
                    f"<td>{sum(x >= 10000 for x in v)} of {len(v)}</td></tr>" for m, v in months.items())
    return (f'<figure class="chart cal-fig" data-mode="{esc(modes[0]["id"])}">'
            f'<div class="cal-modes" role="group" aria-label="Highlight">{buttons}</div>'
            f'{_cal_svg(days, 53, 16, "cal-wide", "cw", title, desc)}{_cal_svg(days, 27, 12, "cal-narrow", "cn", title, desc)}'
            f'<div class="cal-legend">Daily steps: {legend}</div>'
            f'<figcaption>{esc(caption)}</figcaption>'
            f'<details class="chart-data"><summary>{esc(table_label)}</summary><table><thead><tr><th>Month</th>'
            f'<th>Median steps</th><th>Days with 10,000+</th></tr></thead><tbody>{table}</tbody></table></details>'
            f'</figure>')


def _weekly(days: list[dict], start: date, end: date, key: str) -> list[tuple[date, float]]:
    weeks = {}
    for d in days:
        if start <= d["date"] <= end:
            weeks.setdefault(d["date"] - timedelta(days=d["date"].weekday()), []).append(d[key])
    return [(w, mean(v)) for w, v in sorted(weeks.items())]


def _panel(series, x, y0, ph, lo, hi, fmt, label, font) -> list[str]:
    y = lambda v: y0 + ph - (v - lo) / (hi - lo) * ph  # noqa: E731
    pts = " ".join(f"{x(d):.1f},{y(v):.1f}" for d, v in series)
    return [f'<text class="ch-ann" x="{x(series[0][0]):.1f}" y="{y0 - 6}" font-size="{font}">{esc(label)}</text>',
            f'<line class="ch-grid" x1="{x(series[0][0]):.1f}" x2="{x(series[-1][0]):.1f}" y1="{y0 + ph}" y2="{y0 + ph}"/>',
            f'<text class="ch-lab ch-y" x="{x(series[0][0]) - 6:.1f}" y="{y(hi):.1f}" font-size="{font}">{fmt(hi)}</text>',
            f'<text class="ch-lab ch-y" x="{x(series[0][0]) - 6:.1f}" y="{y(lo):.1f}" font-size="{font}">{fmt(lo)}</text>',
            f'<polyline class="ch-line" points="{pts}"/>']


def _lines_svg(panels, marker: date, marker_label: str, cls, w, h, font, tag, title, desc) -> str:
    left, right, top, gap = font * 3.4, font * 1.5, 20, 34
    first, last = panels[0][0][0][0], panels[0][0][-1][0]
    span = (last - first).days or 1
    x = lambda d: left + (d - first).days / span * (w - left - right)  # noqa: E731
    ph = (h - top - 24 - gap * (len(panels) - 1)) / len(panels)
    out = [f'<svg class="ch {cls}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{tag}-t {tag}-d">'
           f'<title id="{tag}-t">{esc(title)}</title><desc id="{tag}-d">{esc(desc)}</desc>']
    for i, (series, lo, hi, fmt, label) in enumerate(panels):
        out += _panel(series, x, top + i * (ph + gap), ph, lo, hi, fmt, label, font)
    mx = x(marker)
    out.append(f'<line class="ch-mark" x1="{mx:.1f}" x2="{mx:.1f}" y1="{top - 4}" y2="{h - 22}"/>'
               f'<text class="ch-ann" x="{mx + 4:.1f}" y="{h - 8}" font-size="{font}">{esc(marker_label)}</text>')
    for d in (first, last):
        out.append(f'<text class="ch-lab ch-x" x="{x(d):.1f}" y="{h - 8}" font-size="{font}">{d:%d %b}</text>')
    out.append("</svg>")
    return "".join(out)


def device_check(days, start, end, marker, marker_label, caption, title, desc) -> str:
    """Weekly walking speed and cadence around the day the device's stride estimate changed."""
    speed, cad = _weekly(days, start, end, "speed"), _weekly(days, start, end, "cadence")
    rng = lambda s, pad: (math.floor(min(v for _, v in s) / pad) * pad, math.ceil(max(v for _, v in s) / pad) * pad)  # noqa: E731
    (s_lo, s_hi), (c_lo, c_hi) = rng(speed, 0.1), rng(cad, 1)
    panels = [(speed, s_lo, s_hi, lambda v: f"{v:.1f}", "Walking speed (km/h)"),
              (cad, c_lo, c_hi, lambda v: f"{v:.0f}", "Cadence (steps a minute)")]
    return (f'<figure class="chart">{_lines_svg(panels, marker, marker_label, "ch-wide", 640, 300, 14, "dc-w", title, desc)}'
            f'{_lines_svg(panels, marker, marker_label, "ch-narrow", 360, 300, 12, "dc-n", title, desc)}'
            f'<figcaption>{esc(caption)}</figcaption></figure>')


def _phases_svg(series, phases, cls, w, h, font, tag, title, desc) -> str:
    left, right, top, bottom = font * 3.4, font * 1.5, 18, 26
    first, last = series[0][0], series[-1][0]
    span = (last - first).days or 1
    x = lambda d: left + (d - first).days / span * (w - left - right)  # noqa: E731
    lo = math.floor(min(v for _, v in series) * 10) / 10
    hi = math.ceil(max(v for _, v in series) * 10) / 10
    y = lambda v: top + (h - top - bottom) - (v - lo) / (hi - lo) * (h - top - bottom)  # noqa: E731
    out = [f'<svg class="ch {cls}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{tag}-t {tag}-d">'
           f'<title id="{tag}-t">{esc(title)}</title><desc id="{tag}-d">{esc(desc)}</desc>']
    for p in phases:
        if p.get("shade"):
            out.append(f'<rect class="ch-shade" x="{x(p["start"]):.1f}" y="{top}" width="{x(p["end"]) - x(p["start"]):.1f}" '
                       f'height="{h - top - bottom}"/>')
    for v in (lo, hi):
        out.append(f'<line class="ch-grid" x1="{left}" x2="{w - right}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>'
                   f'<text class="ch-lab ch-y" x="{left - 6}" y="{y(v):.1f}" font-size="{font}">{v:.1f}</text>')
    out.append(f'<polyline class="ch-line ch-thin" points="{" ".join(f"{x(d):.1f},{y(v):.1f}" for d, v in series)}"/>')
    for p in phases:
        m = mean(v for d, v in series if p["start"] <= d <= p["end"])
        out.append(f'<line class="ch-mean" x1="{x(p["start"]):.1f}" x2="{x(p["end"]):.1f}" y1="{y(m):.1f}" y2="{y(m):.1f}"/>'
                   f'<text class="ch-ann" x="{(x(p["start"]) + x(p["end"])) / 2:.1f}" y="{h - 8}" font-size="{font}" '
                   f'text-anchor="middle">{esc(p["label"])}</text>')
    out.append("</svg>")
    return "".join(out)


def phases(days, start, end, phase_list, caption, title, desc) -> str:
    """Weekly walking speed with the program weeks shaded and each period's average drawn across it."""
    series = _weekly(days, start, end, "speed")
    ph = [{**p, "start": date.fromisoformat(p["start"]), "end": date.fromisoformat(p["end"])} for p in phase_list]
    return (f'<figure class="chart">{_phases_svg(series, ph, "ch-wide", 640, 280, 14, "ph-w", title, desc)}'
            f'{_phases_svg(series, ph, "ch-narrow", 360, 260, 12, "ph-n", title, desc)}'
            f'<figcaption>{esc(caption)}</figcaption></figure>')


def effects(rows: list[dict], lo: float, hi: float, caption: str, table_label: str) -> str:
    """Effects in % with 95% intervals (when given) against a zero line, as HTML so the text stays sharp."""
    pos = lambda v: (v - lo) / (hi - lo) * 100  # noqa: E731
    items = []
    for r in rows:
        ci = (f'<span class="fx-ci" style="left:{pos(r["low"]):.1f}%;width:{pos(r["high"]) - pos(r["low"]):.1f}%"></span>'
              if "low" in r else "")
        items.append(f'<li class="fx-row{"" if r.get("clear", True) else " fx-null"}"><span class="fx-label">{esc(r["label"])}'
                     f'</span><span class="fx-track"><span class="fx-zero" style="left:{pos(0):.1f}%"></span>{ci}'
                     f'<span class="fx-dot" style="left:{pos(r["value"]):.1f}%"></span></span>'
                     f'<span class="fx-val">{esc(r["text"])}</span></li>')
    table = "".join(f"<tr><th scope=\"row\">{esc(r['label'])}</th><td>{esc(r['text'])}</td></tr>" for r in rows)
    return (f'<figure class="chart fx"><ol class="fx-rows">{"".join(items)}</ol>'
            f'<div class="fx-axis" aria-hidden="true"><span>{lo:g}%</span><span>0</span><span>+{hi:g}%</span></div>'
            f'<figcaption>{esc(caption)}</figcaption>'
            f'<details class="chart-data"><summary>{esc(table_label)}</summary><table><tbody>{table}</tbody></table></details>'
            f'</figure>')


def picture_link(src: str, alt: str, href: str, label: str, caption: str, width: int, height: int) -> str:
    return (f'<figure class="chart shot"><a class="shot-link" href="{esc(href)}"><img src="{esc(src)}" alt="{esc(alt)}" '
            f'loading="lazy" width="{width}" height="{height}"><span class="shot-cta">{esc(label)}</span></a>'
            f'<figcaption>{esc(caption)}</figcaption></figure>')


def figures(panels: list[dict], caption: str, credit: str) -> str:
    """Published figures shown as images; with several panels, buttons switch between them (the first shows without script)."""
    if len(panels) == 1:
        p = panels[0]
        body = (f'<img src="{esc(p["src"])}" alt="{esc(p["alt"])}" loading="lazy" '
                f'width="{p["width"]}" height="{p["height"]}">')
        return (f'<figure class="chart paper-fig{" wide" if p["width"] > 600 else ""}">{body}<figcaption>{esc(caption)} '
                f'<span class="fig-credit">{esc(credit)}</span></figcaption></figure>')
    buttons = "".join(f'<button type="button" class="cal-mode fig-tab" data-panel="{i}" '
                      f'aria-pressed="{"true" if i == 0 else "false"}">{esc(p["label"])}</button>'
                      for i, p in enumerate(panels))
    imgs = "".join(f'<img class="fig-panel" data-panel="{i}" src="{esc(p["src"])}" alt="{esc(p["alt"])}" '
                   f'width="{p["width"]}" height="{p["height"]}"{"" if i == 0 else " hidden"}>'
                   for i, p in enumerate(panels))
    return (f'<figure class="chart paper-fig fig-tabs"><div class="cal-modes" role="group" aria-label="Panel">{buttons}</div>'
            f'{imgs}<figcaption>{esc(caption)} <span class="fig-credit">{esc(credit)}</span></figcaption></figure>')


def figure_set(name: str, panels: list[dict], caption: str, credit: str, legend: str, measures: list[dict],
               quad: bool = False, table: dict | None = None) -> str:
    """The paper's own figure panels side by side (2 in a row, or 2x2) wherever the figure is at least 600 px wide;
    narrower, a radio switch shows one panel at a time (pure CSS; old browsers show all panels stacked)."""
    opts, cells = [], []
    for i, p in enumerate(panels, 1):
        short, _, story = p["label"].partition("|")
        full = f"{short}: {story}" if story else short
        opts.append(f'<label><input type="radio" name="fs-{esc(name)}" value="{i}"{" checked" if i == 1 else ""} '
                    f'data-name="{esc(full)}"><span class="figset-opt"><span class="figset-tick" aria-hidden="true"></span>'
                    f'{esc(short)}{f"<small>{esc(story)}</small>" if story else ""}</span></label>')
        sub = f'<span class="figset-sub">{esc(p["sub"])}</span>' if p.get("sub") else ""
        title = (f'<p class="figset-title"><strong>{esc(p["title"])}</strong>'
                 f'{sub}</p>'
                 if p.get("title") else "")
        cells.append(f'<div class="figset-panel" data-p="{i}">{title}<a class="figset-img" href="{esc(p["src"])}" '
                     f'aria-label="Open full size: {esc(full)}"><img src="{esc(p["src"])}" alt="{esc(p["alt"])}" '
                     f'width="{p.get("width", 600)}" height="{p.get("height", 500)}"></a></div>')
    first = panels[0]["label"].partition("|")
    first_full = f"{first[0]}: {first[2]}" if first[2] else first[0]
    switch = (f'<fieldset class="figset-switch"><legend class="figset-instr">{esc(legend)}</legend>'
              f'<div class="figset-opts">{"".join(opts)}</div>'
              f'<p class="figset-status" aria-live="polite" hidden>Showing: {esc(first_full)}</p></fieldset>')
    dl = "".join(f'<div><dt>{esc(m["term"])}</dt><dd>{m.get("text_html", esc(m["text"]))}</dd></div>' for m in measures)
    numbers = ""
    if table:
        head = "".join(f"<th>{esc(h)}</th>" for h in table["head"])
        body = "".join("<tr>" + "".join(f"<td>{esc(str(c))}</td>" if j else f'<th scope="row">{esc(str(c))}</th>'
                                         for j, c in enumerate(r)) + "</tr>" for r in table["rows"])
        numbers = (f'<details class="chart-data"><summary>{esc(table["label"])}</summary><table><thead><tr>{head}</tr>'
                   f'</thead><tbody>{body}</tbody></table><p class="fig-credit">{esc(table["note"])}</p></details>')
    return (f'<figure class="chart figset {"figset-quad" if quad else "figset-pair"}"><div class="figset-cq">{switch}'
            f'<div class="figset-grid">{"".join(cells)}</div></div>'
            f'<figcaption>{esc(caption)} <span class="fig-credit">{esc(credit)}</span></figcaption>'
            f'{f"<dl class=fig-measures>{dl}</dl>" if dl else ""}{numbers}</figure>')
