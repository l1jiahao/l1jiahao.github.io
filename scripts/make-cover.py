#!/usr/bin/env python3
"""从论文 PDF 提取方法图，合成为站点用的封面图。

用法:
    python scripts/make-cover.py paper.pdf --venue ICLR --year 2026 \
        --out assets/images/covers/cover-xxx.png [--figure 1] [--page 3]

不指定 --figure 时，自动在所有图注里挑最像"方法图"的那张
（匹配 framework / overview / architecture / pipeline / schematic 等关键词）。

依赖: pip install pymupdf Pillow
"""

import argparse
import re
import sys

import pymupdf
from PIL import Image, ImageDraw, ImageFont

METHOD_HINTS = (
    "framework", "overview", "architecture", "pipeline", "schematic",
    "workflow", "overall", "illustration of the proposed", "method",
)

CANVAS_W, CANVAS_H = 600, 400
STRIP = 34      # 底部信息条高度
PAD = 14        # 图片与画布边缘的留白


def find_captions(doc):
    """返回 [(页码, 图号, 图注文本, 图注所在的第一个矩形)]"""
    out = []
    for pno in range(doc.page_count):
        page = doc[pno]
        text = page.get_text("text")
        for m in re.finditer(r"(?m)^\s*(?:Figure|Fig\.)\s*(\d+)\s*[:.]\s*(.{0,300})", text):
            num = int(m.group(1))
            cap = re.sub(r"\s+", " ", m.group(2)).strip()
            hits = page.search_for(f"Figure {num}:") or page.search_for(f"Figure {num}.")
            if not hits:
                hits = page.search_for(f"Fig. {num}")
            if hits:
                out.append((pno, num, cap, hits[0]))
    return out


def pick_figure(captions, want=None):
    if want is not None:
        for c in captions:
            if c[1] == want:
                return c
        sys.exit(f"找不到 Figure {want}，可用: {sorted({c[1] for c in captions})}")
    for c in captions:
        if any(h in c[2].lower() for h in METHOD_HINTS):
            return c
    return captions[0] if captions else sys.exit("PDF 里没找到任何图注")


def crop_figure(doc, pno, cap_rect, pad=6):
    """用图注上方的矢量/位图元素推算图片区域"""
    page = doc[pno]
    W, H = page.rect.width, page.rect.height

    blocks = [pymupdf.Rect(b[:4]) for b in page.get_text("blocks")]
    left, right = min(b.x0 for b in blocks), max(b.x1 for b in blocks)

    boxes = [pymupdf.Rect(i["bbox"]) for i in page.get_image_info()]
    boxes += [d["rect"] for d in page.get_drawings()]

    # 页眉区（期刊横幅、DOI、横线）不算图的一部分，排除掉
    header_zone = H * 0.10
    cand = [b for b in boxes
            if b.y1 <= cap_rect.y0 + 2 and b.y1 > header_zone
            and b.width > 8 and b.height > 8
            and b.x0 >= left - 12 and b.x1 <= right + 12]
    if not cand:
        sys.exit("图注上方没有找到图形元素")

    x0 = min(b.x0 for b in cand); x1 = max(b.x1 for b in cand)
    y0 = min(b.y0 for b in cand); y1 = max(b.y1 for b in cand)

    above = [t for t in blocks if t.y1 <= y0 + 1]   # 别把上方正文带进来
    if above:
        y0 = max(y0, max(t.y1 for t in above) + 1)

    rect = pymupdf.Rect(max(0, x0 - pad), max(0, y0 - pad),
                        min(W, x1 + pad), min(cap_rect.y0, y1 + pad))
    return page.get_pixmap(clip=rect, dpi=200)


def make_cover(pix, out, venue, year, crop=None):
    fig_path = "/tmp/_figure_tmp.png"
    pix.save(fig_path)
    fig = Image.open(fig_path).convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        fig = fig.crop((int(fig.width * x0), int(fig.height * y0),
                        int(fig.width * x1), int(fig.height * y1)))

    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), "white")
    d = ImageDraw.Draw(canvas)

    avail_w, avail_h = CANVAS_W - PAD * 2, CANVAS_H - STRIP - PAD * 2
    s = min(avail_w / fig.width, avail_h / fig.height)
    nw, nh = max(1, int(fig.width * s)), max(1, int(fig.height * s))
    fig = fig.resize((nw, nh), Image.LANCZOS)
    canvas.paste(fig, ((CANVAS_W - nw) // 2, PAD + (avail_h - nh) // 2))

    d.rectangle([0, 0, CANVAS_W - 1, CANVAS_H - 1], outline="#e5e7eb", width=1)
    d.rectangle([0, CANVAS_H - STRIP, CANVAS_W - 1, CANVAS_H - 1], fill="#f8f9fa")
    d.line([0, CANVAS_H - STRIP, CANVAS_W, CANVAS_H - STRIP], fill="#e5e7eb", width=1)

    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 12)
    d.text((PAD, CANVAS_H - STRIP + 11), venue.upper(), font=font, fill="#6b7280")
    yw = d.textlength(str(year), font=font)
    d.text((CANVAS_W - PAD - yw, CANVAS_H - STRIP + 11), str(year), font=font, fill="#6b7280")

    canvas.save(out, optimize=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--venue", required=True)
    ap.add_argument("--year", required=True, type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--figure", type=int, default=None)
    ap.add_argument("--page", type=int, default=None, help="1-based，配合 --figure 精确定位")
    ap.add_argument("--crop", default=None,
                    help="裁切比例 x0,y0,x1,y1（0~1），宽幅图只取核心 panel 时用，"
                         "例如 --crop 0.34,0,1,1")
    a = ap.parse_args()

    doc = pymupdf.open(a.pdf)
    caps = find_captions(doc)
    print(f"{len(caps)} 个图注:")
    for pno, num, cap, _ in caps:
        print(f"  p{pno+1:2d} Fig{num:<3d} {cap[:88]}")

    if a.page is not None:
        caps = [c for c in caps if c[0] == a.page - 1] or sys.exit("该页没有图注")

    pno, num, cap, rect = pick_figure(caps, a.figure)
    print(f"\n选用: p{pno+1} Figure {num} — {cap[:70]}")
    pix = crop_figure(doc, pno, rect)
    print(f"裁剪: {pix.width}x{pix.height}px")
    crop = None
    if a.crop:
        crop = tuple(float(x) for x in a.crop.split(","))
        assert len(crop) == 4, "--crop 需要 4 个 0~1 的数"
    print("输出:", make_cover(pix, a.out, a.venue, a.year, crop))


if __name__ == "__main__":
    main()
