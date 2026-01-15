def fen_to_sfen(l):
    cs = l.split(" ")
    color = "w" if cs[1] == "b" else "b"
    onboard, hand = cs[0].split("[")
    pchar = " "
    pcount = 0
    hlist = []
    for c in hand:
        if c == "]":
            break
        if c != pchar:
            if pcount > 1:
                hlist.append(str(pcount))
            if pcount > 0:
                hlist.append(pchar)
            pcount = 0
            pchar = c
        pcount += 1
    if pcount == 0:
        hlist.append("-")
    else:
        if pcount > 1:
            hlist.append(str(pcount))
        hlist.append(pchar)
    return f"{onboard} {color} {''.join(hlist)} 0"


print("setoption name Threads value 1")
print("isready")

while True:
    try:
        l = input()
    except EOFError:
        break
    print(f"position sfen {fen_to_sfen(l)}")
    print("go nodes 1000000")
