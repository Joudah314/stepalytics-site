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
        body = (f'<div class="figset-svg">{p["svg_html"]}</div>' if p.get("svg_html") else
                f'<a class="figset-img" href="{esc(p["src"])}" aria-label="Open full size: {esc(full)}"><img src="{esc(p["src"])}" '
                f'alt="{esc(p["alt"])}" width="{p.get("width", 600)}" height="{p.get("height", 500)}"></a>')
        cells.append(f'<div class="figset-panel" data-p="{i}">{title}{body}</div>')
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
    kind = "figset-trio" if len(panels) == 3 else "figset-quad" if quad else "figset-pair"
    return (f'<figure class="chart figset {kind}"><div class="figset-cq">{switch}'
            f'<div class="figset-grid">{"".join(cells)}</div></div>'
            f'<figcaption>{esc(caption)} <span class="fig-credit">{esc(credit)}</span></figcaption>'
            f'{f"<dl class=fig-measures>{dl}</dl>" if dl else ""}{numbers}</figure>')


# --- Air-HOLP figures, redrawn from the paper's data in the page's style ---------------------------------------------
METHOD_STYLE = {  # colour, dash, marker; the same encodings across every figure
    "Air-HOLP": ("#018182", "", "dot"), "Ridge-HOLP": ("#d9733b", "7 5", "square"), "r = 10": ("#d9733b", "7 5", "square"),
    "r = 50": ("#b25a26", "7 5", "diamond"), "r = 200": ("#8a4119", "7 5", "triangle"), "r = 600": ("#5c2a0e", "7 5", "box"),
    "SIS": ("#8e5bb8", "2 5", "ring"), "Ridge-OLS": ("#012150", "2 5", "triangle"),
}


def _dash(d: str) -> str:
    return f' stroke-dasharray="{d}"' if d else ""


def _marker(kind: str, x: float, y: float, colour: str, tip: str) -> str:
    t = f"<title>{esc(tip)}</title>"
    if kind == "dot":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{colour}">{t}</circle>'
    if kind == "ring":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#fff" stroke="{colour}" stroke-width="2.5">{t}</circle>'
    if kind == "square":
        return f'<rect x="{x - 5:.1f}" y="{y - 5:.1f}" width="10" height="10" fill="{colour}">{t}</rect>'
    if kind == "box":
        return (f'<rect x="{x - 5:.1f}" y="{y - 5:.1f}" width="10" height="10" fill="#fff" stroke="{colour}" '
                f'stroke-width="2.5">{t}</rect>')
    if kind == "diamond":
        return (f'<path d="M{x:.1f},{y - 7:.1f} L{x + 7:.1f},{y:.1f} L{x:.1f},{y + 7:.1f} L{x - 7:.1f},{y:.1f}Z" '
                f'fill="{colour}">{t}</path>')
    return f'<path d="M{x:.1f},{y - 7:.1f} L{x + 7:.1f},{y + 5:.1f} L{x - 7:.1f},{y + 5:.1f}Z" fill="{colour}">{t}</path>'


def _legend(names: list[str], w: float, x0: float = 0) -> str:
    widths = [44 + len(n) * 8.4 for n in names]
    x = x0 + (w - sum(widths)) / 2
    out = []
    for n, wd in zip(names, widths):
        c, dash, mk = METHOD_STYLE[n]
        out.append(f'<line x1="{x:.1f}" x2="{x + 30:.1f}" y1="16" y2="16" stroke="{c}" stroke-width="2.5"{_dash(dash)}/>'
                   f'{_marker(mk, x + 15, 16, c, n)}<text class="pf-leg" x="{x + 36:.1f}" y="21">{esc(n)}</text>')
        x += wd
    return "".join(out)


def _frame(w, h, l, r, t, b, x_label, y_label, title, desc):
    return (f'<svg class="pf" viewBox="0 0 {w} {h}" role="img"><title>{esc(title)}</title><desc>{esc(desc)}</desc>'
            f'<rect class="pf-plot" x="{l}" y="{t}" width="{w - l - r}" height="{h - t - b}"/>'
            f'<text class="pf-axis" x="{l + (w - l - r) / 2:.0f}" y="{h - 8}" text-anchor="middle">{esc(x_label)}</text>'
            f'<text class="pf-axis" transform="translate(18 {t + (h - t - b) / 2:.0f}) rotate(-90)" '
            f'text-anchor="middle">{esc(y_label)}</text>')


def line_panel(x: list, series: dict, xlim, ylim, xticks, yticks, x_label, y_label, title, desc, fmt=None) -> str:
    """One of the paper's line charts: the same series, markers and axes, drawn in the page's style."""
    fmt = fmt or (lambda v: f"{v:g}")
    w, h, l, r, t, b = 600, 470, 74, 18, 40, 58
    X = lambda v: l + (v - xlim[0]) / (xlim[1] - xlim[0]) * (w - l - r)  # noqa: E731
    Y = lambda v: t + (1 - (v - ylim[0]) / (ylim[1] - ylim[0])) * (h - t - b)  # noqa: E731
    out = [_frame(w, h, l, r, t, b, x_label, y_label, title, desc), _legend(list(series), w)]
    for v in yticks:
        out.append(f'<line class="pf-grid" x1="{l}" x2="{w - r}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                   f'<text class="pf-tick" x="{l - 8}" y="{Y(v) + 5:.1f}" text-anchor="end">{fmt(v)}</text>')
    for v in xticks:
        out.append(f'<line class="pf-grid" x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{t}" y2="{h - b}"/>'
                   f'<text class="pf-tick" x="{X(v):.1f}" y="{h - b + 22}" text-anchor="middle">{v:,g}</text>')
    for name in reversed(list(series)):
        c, dash, mk = METHOD_STYLE[name]
        pts = " ".join(f"{X(a):.1f},{Y(v):.1f}" for a, v in zip(x, series[name]))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c}" '
                   f'stroke-width="{3 if name == "Air-HOLP" else 2.5}"{_dash(dash)}/>')
        out += [_marker(mk, X(a), Y(v), c, f"{name}: {v:.3f} at {a:g}") for a, v in zip(x, series[name])]
    out.append("</svg>")
    return "".join(out)


def heat_panel(z: list[list[float]], n: list, p: list, label: str, diff: bool, title: str, desc: str) -> str:
    """One heat map of Figure 2 (rows p, columns n), each cell's value printed as in the paper."""
    w, h, l, t, b = 420, 380, 78, 36, 60
    cell_w, cell_h = (w - l - 10) / len(n), (h - t - b) / len(p)
    out = [f'<svg class="pf" viewBox="0 0 {w} {h}" role="img"><title>{esc(title)}</title><desc>{esc(desc)}</desc>'
           f'<text class="pf-head" x="{l + (w - l - 10) / 2:.0f}" y="22" text-anchor="middle">{esc(label)}</text>']
    for i, pv in enumerate(p):
        y = t + (len(p) - 1 - i) * cell_h
        out.append(f'<text class="pf-tick" x="{l - 8}" y="{y + cell_h / 2 + 5:.1f}" text-anchor="end">{pv:,}</text>')
        for j, nv in enumerate(n):
            v = z[i][j]
            a = min(abs(v), 1)
            if diff:
                fill = (f"rgba(31,110,54,{0.08 + 0.9 * a:.2f})" if v > 0 else
                        f"rgba(179,38,30,{0.08 + 0.9 * a:.2f})" if v < 0 else "#eef1f3")
            else:
                fill = f"rgba(1,129,130,{0.06 + 0.94 * v:.2f})"
            dark = a > 0.55
            txt = "0" if abs(v) < 0.005 else f"{v:.2f}".rstrip("0").rstrip(".")
            out.append(f'<rect x="{l + j * cell_w + 1:.1f}" y="{y + 1:.1f}" width="{cell_w - 2:.1f}" height="{cell_h - 2:.1f}" '
                       f'rx="3" fill="{fill}"><title>n = {nv:,}, p = {pv:,}: {v:.3f}</title></rect>'
                       f'<text class="pf-cell{" on" if dark else ""}" x="{l + (j + 0.5) * cell_w:.1f}" '
                       f'y="{y + cell_h / 2 + 6:.1f}" text-anchor="middle">{txt}</text>')
    for j, nv in enumerate(n):
        out.append(f'<text class="pf-tick" x="{l + (j + 0.5) * cell_w:.1f}" y="{h - b + 22}" text-anchor="middle">{nv:,}</text>')
    out.append(f'<text class="pf-axis" x="{l + (w - l - 10) / 2:.0f}" y="{h - 10}" text-anchor="middle">n</text>'
               f'<text class="pf-axis" transform="translate(16 {t + (h - t - b) / 2:.0f}) rotate(-90)" '
               f'text-anchor="middle">p</text></svg>')
    return "".join(out)


def box_panel(cats: list[str], boxes: list[dict], methods: list[str], ylim, yticks, x_label, y_label, title, desc,
              lines: list | None = None, fmt=None, single: bool = False) -> str:
    """The paper's box plots (median, quartiles, whiskers to 1.5 IQR, outliers), drawn in the page's style."""
    fmt = fmt or (lambda v: f"{v:g}")
    w, h, l, r, t, b = 600, 470, 74, 18, 40, 58
    Y = lambda v: t + (1 - (v - ylim[0]) / (ylim[1] - ylim[0])) * (h - t - b)  # noqa: E731
    slot = (w - l - r) / len(cats)
    out = [_frame(w, h, l, r, t, b, x_label, y_label, title, desc)]
    if not single:
        out.append(_legend(methods, w - 170 if lines else w))
    for v in yticks:
        out.append(f'<line class="pf-grid" x1="{l}" x2="{w - r}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                   f'<text class="pf-tick" x="{l - 8}" y="{Y(v) + 5:.1f}" text-anchor="end">{fmt(v)}</text>')
    for i, cat in enumerate(cats):
        cx = l + (i + 0.5) * slot
        out.append(f'<text class="pf-tick" x="{cx:.1f}" y="{h - b + 22}" text-anchor="middle">{esc(cat)}</text>')
        bw = min(slot * 0.34, 70)
        ms = [cat] if single else methods
        for k, m in enumerate(ms):
            c = METHOD_STYLE[m][0]
            x0 = cx + (k - len(ms) / 2) * (bw + 4) + 2
            bx = boxes[i][m]
            out.append(
                f'<g><title>{esc(m)}, {esc(cat)}: median {bx["med"]:.2f}, quartiles {bx["q1"]:.2f} to {bx["q3"]:.2f}</title>'
                f'<line x1="{x0 + bw / 2:.1f}" x2="{x0 + bw / 2:.1f}" y1="{Y(bx["hi"]):.1f}" y2="{Y(bx["lo"]):.1f}" '
                f'stroke="#333" stroke-width="1.5"/>'
                f'<rect x="{x0:.1f}" y="{Y(bx["q3"]):.1f}" width="{bw:.1f}" height="{max(Y(bx["q1"]) - Y(bx["q3"]), 1.5):.1f}" '
                f'fill="{c}" stroke="#333" stroke-width="1.5" rx="2"/>'
                f'<line x1="{x0:.1f}" x2="{x0 + bw:.1f}" y1="{Y(bx["med"]):.1f}" y2="{Y(bx["med"]):.1f}" stroke="#fff" stroke-width="3"/>'
                + "".join(f'<circle cx="{x0 + bw / 2:.1f}" cy="{Y(o):.1f}" r="2.6" fill="none" stroke="#333" stroke-width="1"/>'
                          for o in bx["out"]) + "</g>")
    for name, value, dash, colour in (lines or []):
        out.append(f'<line x1="{l}" x2="{w - r}" y1="{Y(value):.1f}" y2="{Y(value):.1f}" stroke="{colour}" '
                   f'stroke-width="2"{_dash(dash)}/>')
    x = w - 165
    for k, (name, value, dash, colour) in enumerate(lines or []):
        out.append(f'<line x1="{x + k * 82}" x2="{x + k * 82 + 26}" y1="16" y2="16" stroke="{colour}" stroke-width="2"{_dash(dash)}/>'
                   f'<text class="pf-leg" x="{x + k * 82 + 31}" y="21">{esc(name)}</text>')
    out.append("</svg>")
    return "".join(out)


def band_bar(bands: list, caption: str, label: str) -> str:
    """All settings in one bar, split by how far Air-HOLP was above or below Ridge-HOLP: red below, grey equal, green above."""
    colours = ["#b3261e", "#e8908a", "#d5dadd", "#a8d5b0", "#6bb67a", "#3a9150", "#1f6e36", "#0b4a20"]
    total = sum(c for _, c in bands)
    segs, rows = [], []
    for (name, c), col in zip(bands, colours):
        share = c / total * 100
        on = col in ("#b3261e", "#3a9150", "#1f6e36", "#0b4a20")
        lab = f'<span class="bb-in{" on" if on else ""}">{share:.0f}%</span>' if share >= 6 else ""
        segs.append(f'<span class="bb-seg" style="flex:{c} 0 0;background:{col}" '
                    f'title="{esc(name)}: {c:,} settings ({share:.1f}%)">{lab}</span>')
        rows.append(f'<li><span class="bb-sw" style="background:{col}"></span><span class="bb-name">{esc(name)}</span>'
                    f'<span class="bb-num">{share:.1f}%</span><span class="bb-cnt">{c:,} settings</span></li>')
    lower = sum(c for n, c in bands if n.startswith("Lower")) / total * 100
    higher = sum(c for n, c in bands if n.startswith("Higher")) / total * 100
    return (f'<figure class="chart bb"><div class="bb-ends"><span class="bb-lo">Air-HOLP lower: {lower:.0f}%</span>'
            f'<span class="bb-hi">Air-HOLP higher: {higher:.0f}%</span></div>'
            f'<div class="bb-bar" role="img" aria-label="{esc(label)}">{"".join(segs)}</div>'
            f'<ol class="bb-list">{"".join(rows)}</ol><figcaption>{esc(caption)}</figcaption></figure>')


def _nice(lo: float, hi: float, step: float) -> tuple[float, float, list[float]]:
    a, b = math.floor(lo / step) * step, math.ceil(hi / step) * step
    ticks = [round(a + i * step, 6) for i in range(int(round((b - a) / step)) + 1)]
    return a, b, ticks


def airholp_svgs(d: dict) -> dict:
    """Every figure of the Air-HOLP paper, from its own data, as inline charts keyed for the page's panels."""
    out = {}
    two = lambda v: f"{v:.2f}"  # noqa: E731
    for key, f in zip(("fig1a", "fig1b"), d["fig1"]):
        out[key] = line_panel(f["x"], f["series"], (-0.03, 0.93), (0, 1), [0, 0.3, 0.6, 0.9], [0, 0.25, 0.5, 0.75, 1],
                              "Correlation (ρ)", "Sure screening probability", "Sure screening probability against correlation",
                              "Air-HOLP, Ridge-HOLP with r = 10, 50, 200 and 600, and SIS, at correlations 0 to 0.9.", two)
    g = d["fig2"]
    diff = [[round(a - r, 2) for a, r in zip(ra, rr)] for ra, rr in zip(g["air"], g["ridge"])]
    for key, z, lab, is_diff in (("fig2a", g["air"], "Air-HOLP", False), ("fig2b", g["ridge"], "Ridge-HOLP", False),
                                 ("fig2c", diff, "Difference", True)):
        out[key] = heat_panel(z, g["n"], g["p"], lab, is_diff, f"Sure screening probability: {lab}",
                              "Rows are the number of features p, columns the sample size n; each cell shows its value.")
    for key, f, cats, xl in (("fig3a", d["fig3"][0], ["0.25", "0.5", "0.75", "0.9", "0.95"], "Theoretical R²"),
                             ("fig3b", d["fig3"][1], ["3", "6", "9", "12", "15"], "Number of true features (p₀)")):
        boxes = [{"Air-HOLP": b["air"], "Ridge-HOLP": b["ridge"]} for b in f["boxes"]]
        vals = [v for b in f["boxes"] for m in ("air", "ridge") for v in [b[m]["lo"], b[m]["hi"]] + b[m]["out"]] + [f["logp"], f["cut"]]
        lo, hi, ticks = _nice(min(vals), max(vals), 1)
        out[key] = box_panel(cats, boxes, ["Air-HOLP", "Ridge-HOLP"], (lo, hi), ticks, xl, "log(Sure screening threshold)",
                             "Sure screening threshold, Air-HOLP and Ridge-HOLP",
                             "Box plots of the log sure screening threshold; the dashed line is n/log(n), the dotted line p.",
                             [("n/log(n)", f["cut"], "7 5", "#b3261e"), ("p", f["logp"], "2 4", "#333")])
    for key, f in zip(("fig4a", "fig4b", "fig4c", "fig4d"), d["fig4"]):
        vals = [v for s in f["series"].values() for v in s]
        lo, hi, ticks = _nice(min(vals) - 0.01, max(vals) + 0.01, 0.05 if max(vals) - min(vals) < 0.3 else 0.1)
        out[key] = line_panel(list(range(1, 9)), f["series"], (0.7, 8.3), (lo, hi), [2, 4, 6, 8], ticks, "Model size",
                              "Maximum multiple correlation coefficient", "Maximum multiple R against model size",
                              "Air-HOLP, Ridge-HOLP and SIS for models of 1 to 8 genes.", two)
    f = d["fig5"][0]
    vals = [v for s in f["series"].values() for v in s]
    lo, hi, ticks = _nice(min(vals), max(vals), 2)
    out["fig5a"] = line_panel(f["x"], f["series"], (0, 6800), (lo, hi), [0, 2000, 4000, 6000], ticks,
                              "Number of features (p)", "log(Execution time (ms))", "Execution time against the number of features",
                              "Air-HOLP, Ridge-HOLP and Ridge-OLS; 10%-trimmed mean of 10 runs.")
    bx = d["fig5"][1]["boxes"]
    vals = [v for b in bx.values() for v in [b["lo"], b["hi"]] + b["out"]]
    lo, hi, ticks = _nice(min(vals) - 0.02, max(vals) + 0.02, 0.05)
    out["fig5b"] = box_panel(["Air-HOLP", "Ridge-HOLP"], [{"Air-HOLP": bx["Air-HOLP"]}, {"Ridge-HOLP": bx["Ridge-HOLP"]}],
                             ["Air-HOLP", "Ridge-HOLP"], (lo, hi), ticks, "Method", "Execution time (seconds)",
                             "Execution time of Air-HOLP and Ridge-HOLP", "Box plots of 10 runs each.", None, two, single=True)
    return out
