#############################################################################
### Търсене и извличане на информация. Приложение на дълбоко машинно обучение
### Стоян Михов
### Зимен семестър 2025/2026
#############################################################################

### Домашно задание 1
###
### За да работи програмата трябва да се свали корпус от публицистични текстове за Югоизточна Европа,
### предоставен за некомерсиално ползване от Института за български език - БАН
###
### Корпусът може да бъде свален от:
### Отидете на http://dcl.bas.bg/BulNC-registration/#feeds/page/2
### И Изберете:
###
### Корпус с новини
### Корпус от публицистични текстове за Югоизточна Европа.
### 27.07.2012 Български
###	35337  7.9M
###
### Архивът трябва да се разархивира в директорията, в която е програмата.
###
### Преди да се стартира програмата е необходимо да се активира съответното обкръжение с командата:
### conda activate tii
###
### Ако все още нямате създадено обкръжение прочетете файла README.txt за инструкции

import langmodel
import math
import numpy as np

# За да печата кирилица
import sys
sys.stdout.reconfigure(encoding='utf-8')

def editDistance(s1 : str, s2 : str) -> np.ndarray:
	#### функцията намира модифицираното разстояние на Левенщайн между два низа, описано в условието на заданието
	#### вход: низовете s1 и s2
	#### изход: матрицата M с разстоянията между префиксите на s1 и s2 (виж по-долу)

	M = np.zeros((len(s1)+1,len(s2)+1))
	#### M[i,j] следва да съдържа разстоянието между префиксите s1[:i] и s2[:j]
	#### M[len(s1),len(s2)] следва да съдържа разстоянието между низовете s1 и s2
	#### За справка разгледайте алгоритъма editDistance от слайдовете на Лекция 1
	
	#############################################################################
	#### Начало на Вашия код. На мястото на pass се очакват 10-30 реда

	n = len(s1)
	m = len(s2)

	# базови случаи: разстояние до празен низ
	for i in range(1, n + 1):
		M[i, 0] = i      # само изтривания
	for j in range(1, m + 1):
		M[0, j] = j      # само вмъквания


	# основен цикъл
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			# 2. изтриване
			delete_cost = M[i - 1, j] + 1

			# 3. вмъкване
			insert_cost = M[i, j - 1] + 1

			# 4. съвпадение/субституция
			subst_cost = M[i - 1, j - 1] + (0 if s1[i - 1] == s2[j - 1] else 1)

			best = min(delete_cost, insert_cost, subst_cost)
	
			# 5. разцепване
			if j >= 2:   
				merge_w = M[i - 1, j - 2] + 1
				best = min(best, merge_w)

			# 6. сливане
			if i >= 2:   
				merge_p = M[i - 2, j - 1] + 1
				best = min(best, merge_p)

			M[i, j] = best

	#### Край на Вашия код
	#############################################################################

	return M

def editWeight(s1 : str, s2 : str, Weight : dict[tuple[str,str],float]) -> float:
	#### функцията editWeight намира теглото между два низа
	#### вход: низовете s1 и s2, както и речник Weight, съдържащ теглото на всяка от елементарните редакции 
	#### изход: минималната сума от теглата на елементарните редакции, необходими да се получи от единия низ другия
	
	#############################################################################
	#### Начало на Вашия код. На мястото на pass се очакват 15-30 реда

	n, m = len(s1), len(s2)

	M = np.full((n + 1, m + 1), math.inf)
	M[0, 0] = 0.0

 	# базови случаи: превръщане в празен низ 
	for i in range(1, n + 1):
		op = (s1[i - 1], "")               # Del
		w = Weight.get(op, math.inf)
		M[i, 0] = M[i - 1, 0] + w

	for j in range(1, m + 1):
		op = ("", s2[j - 1])               # Ins
		w = Weight.get(op, math.inf)
		M[0, j] = M[0, j - 1] + w

	for i in range(1, n + 1):
		for j in range(1, m + 1):
			best = math.inf

			# Del
			op = (s1[i - 1], "")
			w = Weight.get(op, math.inf)
			best = min(best, M[i - 1, j] + w)

			# Ins
			op = ("", s2[j - 1])
			w = Weight.get(op, math.inf)
			best = min(best, M[i, j - 1] + w)

			# Id
			if s1[i - 1] == s2[j - 1]:
				op = (s1[i - 1], s2[j - 1])   
				w = Weight.get(op, 0.0)
				best = min(best, M[i - 1, j - 1] + w)

			# Sub
			else:
				op = (s1[i - 1], s2[j - 1])   
				w = Weight.get(op, math.inf)
				best = min(best, M[i - 1, j - 1] + w)


			# Spl
			if j >= 2:
				op = (s1[i - 1], s2[j - 2:j])
				if op in Weight:
					best = min(best, M[i - 1, j - 2] + Weight[op])

			# Mrg
			if i >= 2:
				op = (s1[i - 2:i], s2[j - 1])
				if op in Weight:
					best = min(best, M[i - 2, j - 1] + Weight[op])

			M[i, j] = best

	return float(M[n, m])


	#### Край на Вашия код
	#############################################################################


def bestAlignment(s1 : str, s2 : str) -> list[tuple[str,str]]:
	#### функцията намира подравняване с минимално тегло между два низа 
	#### вход: 
	####	 низовете s1 и s2
	#### изход: 
	####	 списък от елементарни редакции, подравняващи s1 и s2 с минимално тегло


	M = editDistance(s1, s2)
	alignment = []
	
	#############################################################################
	#### УПЪТВАНЕ:
	#### За да намерите подравняване с минимално тегло следва да намерите път в матрицата M,
	#### започващ от последния елемент на матрицата -- M[len(s1),len(s2)] до елемента M[0,0]. 
	#### Всеки преход следва да съответства на елементарна редакция, която ни дава минимално
	#### тегло, съответстващо на избора за получаването на M[i,j] във функцията editDistance.
	#### Събирайки съответните елементарни редакции по пъта от M[len(s1),len(s2)] до M[0,0] 
	#### в обратен ред ще получим подравняване с минимално тегло между двата низа.
	#### Всяка елементарна редакция следва да се представи като двойка низове.
	#### ПРЕМЕР:
	#### bestAlignment('редакция','рдашиа') = [('р','р'),('е',''),('д' 'д'),('а','а'),('кц','ш'),('и','и'),('я','а')]
	#### ВНИМАНИЕ:
	#### За някой двойки от думи може да съществува повече от едно подравняване с минимално тегло.
	#### Достатъчно е да изведете едно от подравняванията с минимално тегло.
	#############################################################################	
	
	#############################################################################	
	#### Начало на Вашия код. На мястото на pass се очакват 15-30 реда

	n, m = len(s1), len(s2)
	i, j = n, m

	while i > 0 or j > 0:
		# 1 Id / Sub
		if i > 0 and j > 0 and M[i, j] == M[i - 1, j - 1] + (0 if s1[i - 1] == s2[j - 1] else 1):
			alignment.append((s1[i - 1], s2[j - 1]))
			i -= 1
			j -= 1

		# 2 Merge
		elif (
			i > 1 and j > 0
			and M[i, j] == M[i - 2, j - 1] + 1
			and s1[i - 2] != s2[j - 1]
			and s1[i - 1] != s2[j - 1]
		):
			alignment.append((s1[i - 2:i], s2[j - 1]))
			i -= 2
			j -= 1

		#3 Split
		elif (
			i > 0 and j > 1
			and M[i, j] == M[i - 1, j - 2] + 1
			and s1[i - 1] != s2[j - 2]
			and s1[i - 1] != s2[j - 1]
		):
			alignment.append((s1[i - 1], s2[j - 2:j]))
			i -= 1
			j -= 2

		# 4 Delete
		elif i > 0 and M[i, j] == M[i - 1, j] + 1:
			alignment.append((s1[i - 1], ""))
			i -= 1

		# 5 Insert
		elif j > 0 and M[i, j] == M[i, j - 1] + 1:
			alignment.append(("", s2[j - 1]))
			j -= 1

		else:
			raise RuntimeError(f"Error! i={i}, j={j}")

	alignment.reverse()

			
	#### Край на Вашия код
	#############################################################################
			
	return alignment

def trainWeights(corpus : list[tuple[str,str]]) -> dict[tuple[str,str],float]:
	#### Функцията editionWeights връща речник съдържащ теглото на всяка от елементарните редакции
	#### Функцията реализира статистика за честотата на елементарните редакции от корпус, състоящ се от двойки сгрешен низ и коригиран низ. Теглата са получени след оценка на вероятността за съответната грешка, използвайки принципа за максимално правдоподобие.
	#### Вход: Корпус от двойки сгрешен низ и коригиран низ
	#### изход: речник съдържащ теглото на всяка от елементарните редакции
	
	ids = subs = ins = dels = splits = merges = 0
	for q,r in corpus:
		alignment = bestAlignment(q,r)
		for op in alignment:
			if len(op[0]) == 1 and  len(op[1]) == 1 and op[0] == op[1]: ids += 1
			elif len(op[0]) == 1 and  len(op[1]) == 1: subs += 1
			elif len(op[0]) == 0 and  len(op[1]) == 1: ins += 1
			elif len(op[0]) == 1 and  len(op[1]) == 0: dels += 1
			elif len(op[0]) == 1 and  len(op[1]) == 2: splits += 1
			elif len(op[0]) == 2 and  len(op[1]) == 1: merges += 1
	N = ids + subs + ins + dels + splits + merges

	weight = {}
	for a in langmodel.alphabet:
		weight[(a,a)] = - math.log( ids / N )
		weight[(a,'')] = - math.log( dels / N )
		weight[('',a)] = - math.log( ins / N )
		for b in langmodel.alphabet:
			if a != b:
				weight[(a,b)] = - math.log( subs / N )
			for c in langmodel.alphabet:
				if a != c and b != c:
					weight[(a+b,c)] = - math.log( merges / N )
					weight[(c,a+b)] = - math.log( splits / N )

	return weight


def generateEdits(q : str) -> list[str]:
	### помощната функция, generate_edits по зададена заявка генерира всички възможни редакции на разстояние едно от тази заявка.
	### Вход: заявка като низ q
	### Изход: Списък от низове с модифицирано разстояние на Левенщайн 1 от q
	###
	### В тази функция вероятно ще трябва да използвате азбука, която е дефинирана в langmodel.alphabet
	###
	#############################################################################
	#### Начало на Вашия код. На мястото на pass се очакват 10-20 реда

    alphabet = langmodel.alphabet
    n = len(q)
    edits = set()

    # 1 Delete
    for i in range(n):
        edits.add(q[:i] + q[i+1:])

    # 2 Insert
    for i in range(n + 1):
        for c in alphabet:
            edits.add(q[:i] + c + q[i:])

    # 3 Sub
    for i in range(n):
        for c in alphabet:
            if c != q[i]:
                edits.add(q[:i] + c + q[i+1:])

    # 4 Split
    for i in range(n):
        for a in alphabet:
            for b in alphabet:
                edits.add(q[:i] + a + b + q[i+1:])

    # 5 Merge
    for i in range(n - 1):
        for c in alphabet:
            edits.add(q[:i] + c + q[i+2:])

    return list(edits)


	#### Край на Вашия код
	#############################################################################


def generateCandidates(query : str, dictionary : dict[str, int]) -> list[str]:
	### Започва от заявката query и генерира всички низове НА РАЗСТОЯНИЕ <= 2, за да се получат кандидатите за корекция. 
	### Връщат се единствено кандидати, за които всички думи са в речника dictionary.
		
	### Вход:
	###	 Входен низ: query
	###	 Речник: dictionary

	### Изход:
	###	 Списък от низовете, които са кандидати за корекция
	
	def allWordsInDictionary(q : str) -> bool:
		### Помощна функция, която връща истина, ако всички думи в заявката са в речника
		return all(w in dictionary for w in q.split())


	L=set()
	if allWordsInDictionary(query):
		L.add(query)
	A = generateEdits(query)
	pb = langmodel.progressBar()
	pb.start(len(A))
	for query1 in A:
		if allWordsInDictionary(query1):
			L.add(query1)
		pb.tick()
		for query2 in generateEdits(query1):
			if allWordsInDictionary(query2):
				L.add(query2)
	pb.stop()
	return list(L)



def correctSpelling(r : str, model : langmodel.MarkovModel, weights : dict[tuple[str,str],float], mu : float = 1.0, alpha : float = 0.9):
	### Комбинира вероятността от езиковия модел с вероятността за редактиране на кандидатите за корекция, генерирани от generate_candidates за намиране на най-вероятната желана (коригирана) заявка по дадената оригинална заявка query.
	###
	### Вход:
	###		заявка: r,
	###		езиков модел: model,
	###	 речник съдържащ теглото на всяка от елементарните редакции: weights
	###		тегло на езиковия модел: mu
	###		коефициент за интерполация на езиковият модел: alpha
	### Изход: най-вероятната заявка


	### УПЪТВАНЕ:
	###	Удачно е да работите с логаритъм от вероятностите. Логаритъм от вероятността от езиковия модел може да получите като извикате метода model.sentenceLogProbability. Минус логаритъм от вероятността за редактиране може да получите като извикате функцията editWeight.
	#############################################################################
	#### Начало на Вашия код за основното тяло на функцията correct_spelling. На мястото на pass се очакват 3-10 реда

	candidates = generateCandidates(r, model.kgrams[tuple()])
	#Dprint(candidates)


	best_q = r
	best_score = -math.inf

	for q in candidates:
		words = [w.lower() for w in q.split()]
		sent = [model.startToken] + words + [model.endToken]

		log_p_q = model.sentenceLogProbability(sent, alpha)

		edit_cost = editWeight(r, q, weights)
		log_p_r_given_q = -edit_cost

		score = log_p_r_given_q + mu * log_p_q

		if score > best_score:
			best_score = score
			best_q = q

	return best_q

	#### Край на Вашия код
	#############################################################################


