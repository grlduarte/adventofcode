## Análise

O problema consiste em encontrar todos os números inteiros, dentro de um certo intervalo, que satisfaçam um conjunto de
condições preestabelecidas.

### Input

Nem todo mundo está seguindo o protocolo de ler o *input* genérico, o que dificulta o trabalho de quem quer comparar os
códigos. Não se trata de saber se funciona ou não, e sim de garantir que um *input* não está mais perto da resposta do
que outro. 

### Percorrendo possibilidades

A maneira mais direta de resolver o problema é percorrer todos os números entre o número inicial e final, e testar se
ele satisfaz as condições dadas. A maioria das pessoas fez incrementos de 1 em 1 e testou todos eles. A implementação
destes testes variou:

- Teste de cada condição separadamente e posterior comparação (e.g. Natalia).
- Testes em sequência, ou seja, se satisfaz um passa para o próximo (e.g. Julia).
- Construir uma lista que satisfaz uma condição e aplicar o próximo teste nesta lista (e.g. Katia).

Outra possibilidade é calcular o próximo número possível, já sabendo que o número na posição *i + 1* tem que ser maior
ou igual ao número na posição *i*.

### Verificando se a sequência é crescente

Encontrei basicamente três maneiras de verificar se a sequência é crescente:

- Fazendo um loop para comparar cada número com o número seguinte (e.g. Everton).
- Separando todos os números e comparando par a par (e.g. Victor).
- Comparando o número completo com uma sequência ordenada contendo os mesmos algarismos (e.g. Gabriel)

### Contando repetições

Um dos critérios para uma senha válida era que houvesse números repetidos adjacentes, na primeira parte podia ser
qualquer quantidade de repetições, e na segunda parte deveria ser apenas um par. Em geral as pessoas utilizaram alguma
variação do seguinte: transformar o número em uma *string* e contar repetições dos dígitos, no mais das vezes com o
método *count*.

Ao utilizar o método *count* existe a possibilidade de contar números não adjacentes, de forma que se faz necessário
garantir previamente que a sequência seja crescente, e só então aplicar o *count*.

---

### Algumas recomendações gerais

- Não fazer loops com *np.arange*. Isso consome memória sem necessidade, já que o método retorna um vetor que é
armazenado inteiro na memória. Isso é bem diferente (embora o nome seja quase igual) do que faz a função *range*.

- Cuidar com variáveis globais dentro de funções. Certamente não é proibido, e pode haver situações em que é útil ter
uma variável global, principalmente em um script rápido que se vai utilizar umas poucas vezes. Porém, não é bom
desenvolver esse hábito, entre outras coisas por que conforme o código cresce e se faz operações com essa variável, pode
se tornar muito custoso debugar o código (e.g. por que essa variável não está com o valor que eu coloquei na linha 123?)

- Cuidado com encadeamento de comparativos.

  ```python
  >>> -1 < 0 < 1
  True
  ```

  Porém
  
  ```python
  >>> (-1 < 0) < 1
  False
  ```

---

## Enunciado: Day 4: Secure Container

### Part one

You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on
a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

* It is a six-digit number.
* The value is within the range given in your puzzle input.
* Two adjacent digits are the same (like 22 in 122345).
* Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

* 111111 meets these criteria (double 11, never decreases).
* 223450 does not meet these criteria (decreasing pair of digits 50).
* 123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle answer was **1178**.

### Part two

An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of
matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

* 112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
* 123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
* 111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

How many different passwords within the range given in your puzzle input meet all of the criteria?

Your puzzle answer was **763**.

Your puzzle input was **235741-706948**.
