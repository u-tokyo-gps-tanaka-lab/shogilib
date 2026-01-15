from shogilib import Position, showstate, show_images_hv


def test_images():
    pos = Position.from_fen(
        "+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+l+l+l+l+n+n+n+n+s/+s+s+sb5/6g2/6g1K/5r1g1/8g/5+b1k+r[] b"
    )
    print(pos.fen())
    showstate(pos, filename="tests/state.png")


def test_show_images_hv():
    fenlist = [
        "+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+l+l+l+l+n+n+n+n+s/+s+s+sb5/5+rg2/6g1K/7g1/8g/5+b1k+r[] w",
        "+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+l+l+l+l+n+n+n+n+s/+s+s+sb5/5+rg1K/6g2/7g1/8g/5+b1k+r[] b",
        "+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+l+l+l+l+n+n+n+n+s/+s+s+s6/5+rg1K/6g2/6+bg1/8g/5+b1k+r[] w",
        "+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+l+l+l+l+n+n+n+n+s/+s+s+s6/5+rg2/6g1K/6+bg1/8g/5+b1k+r[] b",
        "+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+l+l+l+l+n+n+n+n+s/+s+s+s6/5+rg2/6ggK/6+b2/8g/5+b1k+r[] w",
        "+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+l+l+l+l+n+n+n+n+s/+s+s+s6/5+rg1K/6gg1/6+b2/8g/5+b1k+r[] b",
        "+p+p+p+p+p+p+p+p+p/+p+p+p+p+p+p+p+p+p/+l+l+l+l+n+n+n+n+s/+s+s+s6/5+rg1K/6gg1/6+b1g/9/5+b1k+r[] w",
    ]
    images = [showstate(Position.from_fen(fen)) for fen in fenlist]
    show_images_hv(images, 4, filename="tests/states.png")
