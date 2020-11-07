import nltk as nl

saying1 = "Those three men in uniform robbed shops in Madaraka"
saying2 = "Three robbed shops have been in Madaraka with men"
saying3 = "Madaraka area has the three shops that were robbed"

saying1_bi_grams = list(nl.bigrams(saying1.lower().split()))
saying2_bi = list(nl.ngrams(saying2.lower().split(), 2))
saying3_bi = list(nl.ngrams(saying3.lower().split(), 2))
saying = saying1 + " " + saying2 + " " + saying3
saying = saying.lower()
bi_saying = list(nl.ngrams(saying.split(), 2))
bi_saying_cnt= saying1_bi_grams + saying2_bi + saying3_bi
print(bi_saying_cnt)
test_input = input("Enter text: ")
bi_test_input = list(nl.ngrams(test_input.lower().split(), 2))
print(bi_test_input)
for t in bi_test_input:
    x = bi_saying_cnt.count(t)/ saying.count(t[0])
    x2 = bi_saying.count(t) / saying.count(t[0])
    print(t)
    print(t[0])
    print(f'X with conct {x}')
    print(f'X2 without conct {x2}')
