from pychord import Chord




## 이걸 제대로 만들어야 된다.
def set_guitar_code(ori_key, transpose="", capo_fret=0):
    c = Chord(ori_key)
    c.transpose(-capo_fret)


    return c

print(set_guitar_code('C', capo_fret=3))