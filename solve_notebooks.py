"""Fill coursework templates; mathematical checks run inside each notebook."""
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parent / 'MDS-new'

def fill(name, replacements, notes=()):
    path = ROOT / name
    nb = nbformat.read(path, as_version=4)
    nb.cells = [cell for cell in nb.cells if not cell.source.startswith('## Решение и проверка')]
    for index, source in replacements.items():
        nb.cells[index].source = source.strip()
        nb.cells[index].outputs = []
        nb.cells[index].execution_count = None
    nb.cells.append(nbformat.v4.new_markdown_cell(
        '## Решение и проверка\n\nРешение подготовлено AI по запросу владельца репозитория. '
        'Выполнение подтверждает работоспособность кода; самостоятельное владение материалом не оценивалось.\n\n'
        + '\n\n'.join(notes)))
    nbformat.write(nb, path)

fill('HW_1_upd.ipynb', {
4: '''import numpy as np
film_1 = np.array([0,0,0,0,1,0])
film_2 = np.array([0,1,0,1,0,0])
film_3 = np.array([0,0,1,1,1,0])
film_4 = np.array([1,0,0,1,0,1])''',
7: '''cosine = film_2 @ film_3 / (np.linalg.norm(film_2) * np.linalg.norm(film_3))
angle = np.degrees(np.arccos(np.clip(cosine, -1, 1)))
assert np.isclose(cosine, 1 / np.sqrt(6))
print(f'Косинусная мера: {cosine:.6f}; угол: {angle:.6f}°')''',
11: '''import sympy as sp
x = sp.symbols('x')
f = 8*x*(x+3)**2
derivative = sp.diff(f, x)
value = derivative.subs(x, 1)
assert value == 192
display(derivative, value)''',
14: '''matrix = np.vstack([film_1, film_2, film_3, film_4])
result = np.array([1,2,3,4]) @ matrix
assert np.array_equal(result, [4,2,3,9,4,4])
print(matrix)
print(result)'''}, ['Скалярное произведение равно 1, нормы — √2 и √3. Производная: 24x² + 96x + 72; в точке 1 равна 192.'])

fill('HW_2_upd.ipynb', {
4: '''import numpy as np
A = np.arange(1, 10).reshape(3,3)
B = A + np.eye(3)
product = B @ np.array([1,2,3])
transpose = B.T
inverse = np.linalg.inv(B)
assert np.allclose(B @ inverse, np.eye(3))
assert np.array_equal(product, [15,34,53])
for title, value in [('A',A), ('A + I',B), ('Произведение',product), ('Транспонирование',transpose), ('Обратная',inverse)]:
    print(title, '\\n', value)''',
8: '''m = np.array([[2,2],[1,3]])
values, vectors = np.linalg.eig(m)
assert np.allclose(m @ vectors, vectors @ np.diag(values))
assert np.allclose(np.sort(values), [1,4])
print('Собственные значения:', values)
print('Собственные векторы — столбцы:', vectors)''',
11: '''C = np.array([[1,1],[1,2]])
assert np.all(C != 0) and np.isclose(np.linalg.det(C), 1)
print(C, 'det =', np.linalg.det(C))'''}, ['Собственные значения 1 и 4. Соответствующие направления векторов: (−2, 1) и (1, 1).'])

fill('HW_3_upd.ipynb', {
6: '''theta = np.deg2rad(130)
S = np.diag([0.5,0.5,1])
R = np.array([[np.cos(theta),-np.sin(theta),0], [np.sin(theta),np.cos(theta),0], [0,0,1]])
F = np.array([[0,1,0],[1,0,0],[0,0,1]])
# Точки записаны строками: умножаем на транспонированную матрицу.
scaled = A @ S.T
rotated = scaled @ R.T
reflected = rotated @ F.T
assert np.allclose(np.linalg.norm(scaled[:,:2],axis=1), np.linalg.norm(A[:,:2],axis=1)/2)
assert np.allclose(reflected[:,:2], rotated[:,[1,0]])
fig, axes = plt.subplots(1,4,figsize=(14,4))
for ax, points, title in zip(axes, [A,scaled,rotated,reflected], ['Исходный','Масштаб ½','Поворот 130°','Отражение y=x']):
    ax.plot(points[:,0],points[:,1], marker='o')
    ax.set(xlim=(-160,160), ylim=(-160,160), title=title)
    ax.set_aspect('equal'); ax.grid()
plt.tight_layout(); plt.show()''',
10: '''m = np.array([[1,2],[2,3]])
values, Q = np.linalg.eigh(m)
Lambda = np.diag(values)
assert np.allclose(Q.T @ Q, np.eye(2))
assert np.allclose(Q @ Lambda @ Q.T, m)
print('Собственные значения:',values)
print('Q:',Q, '\\nΛ:',Lambda, '\\nQΛQᵀ:', Q @ Lambda @ Q.T)'''}, ['Преобразования применены последовательно: масштабирование → поворот против часовой стрелки → отражение. Спектральное разложение: M = QΛQᵀ, λ = 2 ± √5.'])

fill('HW_4_upd.ipynb', {
4: '''import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
x = sp.symbols('x', real=True)
f = x**5 + 4*sp.sin(2*x) + sp.cos(3*x+3)
d1, d2 = sp.diff(f,x), sp.diff(f,x,2)
display(d1, d2)
print('f′(1) =', sp.N(d1.subs(x,1),12))
print('f″(1) =', sp.N(d2.subs(x,1),12))
assert sp.simplify(d1-(5*x**4+8*sp.cos(2*x)-3*sp.sin(3*x+3))) == 0
assert sp.simplify(d2-(20*x**3-16*sp.sin(2*x)-9*sp.cos(3*x+3))) == 0''',
8: '''g = sp.sin(2*x+1)**5
g1, g2 = sp.diff(g,x), sp.diff(g,x,2)
display(g1,g2)
grid = np.linspace(-5,5,2000)
fig, axes = plt.subplots(2,1,figsize=(12,6),sharex=True)
for ax, expr, title in zip(axes,[g1,g2],['Первая производная','Вторая производная']):
    ax.plot(grid, sp.lambdify(x,expr,'numpy')(grid)); ax.set_title(title); ax.grid()
axes[-1].set_xlabel('x'); plt.tight_layout(); plt.show()'''})

fill('HW_5_upd.ipynb', {
4: '''import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
x,y = sp.symbols('x y',real=True)
f1 = 2*x**2*y**3 + 1/x + y**2*x + 7
f2 = x**2*y-sp.sin(x*y)+sp.cos(x**2)+6*y
for expr in [f1,f2]:
    display(sp.diff(expr,x),sp.diff(expr,y))''',
8: '''gradient = sp.Matrix([sp.diff(f1,x),sp.diff(f1,y)])
value = gradient.subs({x:1,y:2})
assert value == sp.Matrix([35,28])
display(gradient,value)''',
11: '''grid = np.linspace(-3,3,120)
X1,X2 = np.meshgrid(grid,grid)
Z = X2**2-X1**2*X2+2*X1*X2
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111,projection='3d')
surface = ax.plot_surface(X1,X2,Z,cmap='viridis')
ax.set(xlabel='x₁',ylabel='x₂',zlabel='f',title='f = x₂² − x₁²x₂ + 2x₁x₂')
fig.colorbar(surface,ax=ax,shrink=0.6); plt.show()'''}, ['Для первой функции область определения: x ≠ 0. Градиент в точке (1, 2): (35, 28).'])

fill('HW_6_upd.ipynb', {6: '''def f(x, a, b):
    return np.exp(a)*np.sin(b*x)+x

rows = []
candidates = []
for method in ['lm','trf','dogbox']:
    for p0 in [(1,1),(3,2),(3.5,2.1)]:
        try:
            params, covariance = curve_fit(f,x,y,p0=p0,method=method,maxfev=10000)
            rmse = np.sqrt(np.mean((np.asarray(y)-f(x,*params))**2))
            rows.append({'method':method,'p0':str(p0),'a':params[0],'b':params[1],'RMSE':rmse})
            candidates.append((rmse,params,covariance))
        except RuntimeError as exc:
            rows.append({'method':method,'p0':str(p0),'error':str(exc)})
display(pd.DataFrame(rows))
best = min(candidates,key=lambda item:item[0])
res = (best[1],best[2])
assert best[0] < 0.01
print('Лучшие параметры:', res[0], 'RMSE:',best[0])'''}, ['Сравниваются методы и начальные приближения по RMSE на заданных точках. Нелинейная подгонка может попасть в локальный минимум; малая ошибка проверяется явно.'])

fill('HW_7_upd.ipynb', {
5: '''import pandas as pd
rows = []
experiments = {
    'strategy':['best1bin','rand1bin','best2bin','randtobest1bin'],
    'popsize':[5,10,15,25,40],
    'mutation':[0.3,0.5,0.7,0.9,(0.5,1.0)]
}
for parameter, values in experiments.items():
    for value in values:
        kwargs = dict(strategy='best1bin',popsize=15,mutation=(0.5,1.0))
        kwargs[parameter] = value
        r = differential_evolution(ackley,bounds,seed=42,polish=False,maxiter=1000,**kwargs)
        rows.append(dict(parameter=parameter,value=str(value),nit=r.nit,nfev=r.nfev,fun=r.fun,success=r.success))
table = pd.DataFrame(rows)
display(table)
fig, axes = plt.subplots(1,3,figsize=(16,4))
for ax, parameter in zip(axes,experiments):
    subset = table[table.parameter==parameter]
    ax.bar(subset.value,subset.nit); ax.set(title=parameter,ylabel='nit'); ax.tick_params(axis='x',rotation=30)
plt.tight_layout(); plt.show()
assert (table.fun < 1e-6).any()''',
9: '''local_rows = []
for method in ['Nelder-Mead','Powell','BFGS']:
    for start in [[0,0],[1,1],[4,4]]:
        r = minimize(ackley,start,method=method,options={'maxiter':2000})
        local_rows.append(dict(method=method,start=str(start),fun=r.fun,nit=r.nit,success=r.success))
display(pd.DataFrame(local_rows))'''}, ['Один параметр меняется при остальных фиксированных. Seed=42 делает прогоны воспроизводимыми в выбранной версии SciPy. nit сравнивается вместе с nfev и качеством результата; один seed не доказывает общий рейтинг методов. Старт (0,0) уже находится в глобальном минимуме Ackley.'])

fill('HW_8_upd.ipynb', {
4: '''import numpy as np
p = np.dot([0.2,0.3,0.5],[0.1,0.05,0.2])
assert np.isclose(p,0.135)
print(f'По формуле полной вероятности: {p:.3f} = {p:.1%}')''',
7: '''from itertools import product,combinations
outcomes = np.array(list(product([0,1],repeat=3)))
events = [outcomes[:,0]==outcomes[:,1],outcomes[:,1]==outcomes[:,2],outcomes[:,0]==outcomes[:,2]]
for i,j in combinations(range(3),2):
    joint = np.mean(events[i]&events[j])
    assert np.isclose(joint,np.mean(events[i])*np.mean(events[j]))
    print(f'P(A{i+1} ∩ A{j+1}) = {joint}; P(A{i+1})P(A{j+1}) = 0.25')
joint_all = np.mean(events[0]&events[1]&events[2])
product_all = np.prod([np.mean(event) for event in events])
assert not np.isclose(joint_all,product_all)
print('Совместная вероятность:',joint_all,'; произведение:',product_all)''',
11: '''import matplotlib.pyplot as plt
from scipy.stats import norm,expon,t
families = [
    ('Нормальное',norm,[{'loc':0,'scale':1},{'loc':2,'scale':1},{'loc':-2,'scale':1},{'loc':0,'scale':0.5},{'loc':0,'scale':2}]),
    ('Экспоненциальное',expon,[{'loc':0,'scale':0.5},{'loc':0,'scale':1},{'loc':0,'scale':2},{'loc':1,'scale':1},{'loc':2,'scale':1}]),
    ('Стьюдента',t,[{'df':1},{'df':2},{'df':5},{'df':30},{'df':5,'loc':2,'scale':2}])
]
grid = np.linspace(-8,10,3000)
fig, axes = plt.subplots(1,3,figsize=(18,5))
for ax,(title,distribution,parameters) in zip(axes,families):
    for params in parameters:
        ax.plot(grid,distribution.pdf(grid,**params),label=str(params))
    ax.set(title=title,xlabel='x',ylabel='pdf'); ax.legend(fontsize=8); ax.grid()
plt.tight_layout(); plt.show()'''}, ['У каждого события вероятность 1/2. Для каждой пары пересечение равно 1/4. Все три происходят лишь для 000 и 111: вероятность 1/4, тогда как произведение вероятностей равно 1/8.', 'loc сдвигает распределение, scale растягивает и снижает высоту плотности. У экспоненциального распределения носитель начинается в loc, среднее loc + scale. У Стьюдента меньшие df дают более тяжёлые хвосты; при df > 1 среднее равно loc, при df > 2 дисперсия scale²·df/(df−2). При больших df приближается к нормальному.'])

fill('HW_9_upd.ipynb', {
4: '''rng = np.random.default_rng(42)
rv = sts.expon(scale=1)
sample = rv.rvs(size=1000,random_state=rng)''',
6: '''sizes = [2,5,10,30,100]
samples_count = 1000
means = {n:rv.rvs(size=(samples_count,n),random_state=rng).mean(axis=1) for n in sizes}
table = pd.DataFrame([{'n':n,'mean':values.mean(),'variance':values.var(ddof=1),'theoretical_variance':1/n} for n,values in means.items()])
display(table)
for n,values in means.items():
    assert values.shape == (1000,)
    assert abs(values.mean()-1) < 5/np.sqrt(n*1000)''',
7: '''fig, axes = plt.subplots(1,len(sizes),figsize=(20,4))
for ax,n in zip(axes,sizes):
    values = means[n]
    ax.hist(values,bins=30,density=True,alpha=0.6,label='Средние 1000 выборок')
    grid = np.linspace(min(values.min(),1-4/np.sqrt(n)),max(values.max(),1+4/np.sqrt(n)),500)
    ax.plot(grid,sts.norm.pdf(grid,loc=1,scale=1/np.sqrt(n)),label='Нормальное приближение')
    ax.set(title=f'n={n}',xlabel='Выборочное среднее',ylabel='Плотность'); ax.legend(fontsize=7)
plt.tight_layout(); plt.show()'''}, ['Выбрано экспоненциальное распределение с E[X]=1 и Var(X)=1. По ЦПТ среднее приближается к N(1, 1/n); стандартное отклонение равно 1/√n. При малых n заметна асимметрия, при росте n форма ближе к нормальной, а разброс уменьшается. Это численная иллюстрация, а не доказательство теоремы.'])

fill('HW_X_upd.ipynb', {
4: '''import sympy as sp
x_symbol = sp.symbols('x',real=True)
expression = sp.tan(sp.sin(x_symbol)+sp.cos(2*x_symbol+3))**2
derivative = sp.diff(expression,x_symbol)
display(derivative)
print('Производная при x=1:',sp.N(derivative.subs(x_symbol,1),12))
fn = sp.lambdify(x_symbol,expression,'numpy')
h=1e-6
assert np.isclose(float(derivative.subs(x_symbol,1)),(fn(1+h)-fn(1-h))/(2*h),rtol=1e-5)''',
9: '''S = np.diag([0.5,1.2,1])
T = np.array([[1,0,200],[0,1,300],[0,0,1]])
scaled = A @ S.T
transformed = scaled @ T.T
assert np.allclose(transformed[:,:2],A[:,:2]*[0.5,1.2]+[200,300])
print('Преобразованные точки:',transformed)
fig,ax = plt.subplots(figsize=(8,6))
for points,title in [(A,'Исходный'),(transformed,'Масштаб → смещение')]:
    ax.plot(points[:,0],points[:,1],marker='o',label=title)
ax.set_aspect('equal'); ax.legend(); ax.grid(); plt.show()''',
13: '''values,vectors = np.linalg.eig(m)
assert np.allclose(np.sort(values),[-1,3])
assert np.allclose(m @ vectors,vectors @ np.diag(values))
print('Собственные значения:',values,'\\nВекторы — столбцы:',vectors)''',
20: '''# Границы — явно выбранная область поиска, не доказательство глобального
# минимума по неограниченной частоте b. Отрицательная b нужна для этих данных.
search_bounds = [(-5,5),(-10,10)]
global_result = differential_evolution(error,search_bounds,seed=42,tol=1e-9,maxiter=1500,polish=False)
local_result = minimize(error,global_result.x,method='Nelder-Mead',options={'xatol':1e-11,'fatol':1e-10,'maxiter':5000})
best = min([global_result,local_result],key=lambda r:r.fun)
print('a, b:',best.x,'; сумма абсолютных ошибок:',best.fun)
assert best.fun < 1e-4
plt.plot(x,fx,'o',label='Данные')
grid = np.linspace(0,5,500)
plt.plot(grid,f(grid,*best.x),label='Подобранная функция')
plt.legend(); plt.grid(); plt.show()''',
25: '''norms = np.linalg.norm(raitings,axis=1)
similarity = (raitings @ raitings.T)/np.outer(norms,norms)
np.fill_diagonal(similarity,-np.inf)
nearest = np.argmax(similarity,axis=1)
assert np.all(nearest != np.arange(len(raitings)))
assert len(nearest)==10
for user,neighbor in enumerate(nearest):
    print(f'({user+1}, {neighbor+1}), cosine={similarity[user,neighbor]:.6f}')'''}, ['Пользователи нумеруются с 1. Сравнение пользователя с самим собой исключено. При равенстве максимальных оценок выбирается первый индекс.', 'Собственные значения матрицы: −1 и 3; направления векторов (−2, 1) и (2, 1).'])

print('Filled 10 notebooks')
