import time,datetime,csv,collections

def gen_range0(t:str):
    '迭代t类型的有趣的取值和权重'
    yield 0, 2
    nl = range(1,10)
    pl = 0.5, 0.5, 0.3, 0.3, 0.5, 0.25, 0.25, 0.25, 0.3
    for i, p in zip(nl, pl):
        if t == 'd':
            yield i, p * 0.9
        else:
            yield i, p
        yield i * 10, p
        if t != 'y':
            yield i * 100, p
            if t == 'd':
                yield i * 1000, p
    yield 99, 0.7
    yield 520, 1.5
    yield 521, 1.3
    yield 999, 0.8
    yield 1314, 1.5

def gen_range(t:str):
    for d, p in gen_range0(t):
        yield d, p
        yield -d, p * 0.9

def ranged(t:str):
    '生成有趣数字字典 数字:权重'
    ans = collections.defaultdict(float)
    for d, p in gen_range(t):
        ans[d] = max(ans[d], p)
    return ans

y_range = ranged('y')
m_range = ranged('m')
d_range = ranged('d')
w_range = ranged('w') # 星期

def read_datas(fn:str):
    with open(fn, 'r', encoding='utf-8') as f:
        for ln in csv.reader(f):
            da = {}
            try:
                y, m, d, s, *_ = ln
                da['y'] = int(y) if y else None
                da['m'] = int(m)
                da['d'] = int(d)
                da['s'] = s
                yield da
            except Exception:
                pass

def data_add(a, dy, dm, dd):
    '对于数据a，加上dy年，dm月，dd日后返回'
    t, dm = divmod(dm + a['m'] - 1, 12)
    a = a.copy()
    a['m'] = dm + 1
    dy += t
    a['y'] += dy
    if dd != 0:
        t = datetime.date(a['y'], a['m'], a['d'])
        t += datetime.timedelta(dd)
        a['y'] = t.year
        a['m'] = t.month
        a['d'] = t.day
    return a

def gen_rems(a):
    '对一个事件迭代可以纪念的数据'
    tips = '年', '个月', '个星期', '天'
    for dy, p1 in y_range.items():
        for dm, p2 in m_range.items():
            pp2 = p1 * p2
            for dw, pw in w_range.items():
                ppw = pp2 * pw
                if ppw < 1:
                    continue
                for dd, p3 in d_range.items():
                    try:
                        da = data_add(a, dy, dm, dd + dw * 7)
                    except Exception:
                        continue
                    p = ppw * p3
                    s1 = []
                    s2 = []
                    for di, dt in zip((dy, dm, dw, dd), tips):
                        if di > 0:
                            s2.append(f'{di}{dt}')
                        elif di < 0:
                            s1.append(f'{-di}{dt}')
                    if s1:
                        t = ''.join(s1)
                        s1 = f'还有{t}，'
                    else:
                        s1 = ''
                    if s2:
                        s2 = ''.join(s2)
                    else:
                        s2 = ''
                    da['s'] = s1 + da['s'] + s2
                    da['p'] = p
                    yield da

def gen_remd(datas):
    '生成日期和[权重,提示]的字典'
    ans = collections.defaultdict(list)
    for a in datas:
        for da in gen_rems(a):
            dt = da['y'], da['m'], da['d']
            p = da['p']
            s = da['s']
            ans[dt].append((p, s))
    return ans

def str_rems(ds,limit=10):
    '将[权重,提示]按权重降序后返回字符串列表'
    ds.sort()
    ds.reverse()
    ans = [p[1] for p in ds if p[0] > 0.3]
    if len(ans) > limit:
        ans = ans[:limit]
    return ans

def main():
    for fn in ('datas.txt','datas_test.txt'):
        try:
            datas = read_datas(fn)
            datas = list(datas)
        except FileNotFoundError:
            continue
        else:
            break
    remd = gen_remd(datas)
    td = time.localtime()
    td = tuple(td[:3])  # 今天
    keys = [p for p in remd if p >= td]  # 今天以及以后的日期
    keys.sort()
    keys = keys[:50]  # 只看前20条数据
    for key in keys:
        y, m, d = key
        dl = remd[key]  # 当天列表
        sl = str_rems(dl)  # 信息列表
        if not sl:
            continue
        print(f'【{y}/{m}/{d}】')
        for s in sl:
            print(s)

if __name__ == '__main__':
    main()
