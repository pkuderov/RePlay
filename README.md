# RePlay
Библиотека RePlay содержит инструменты для создания рекомендательных систем от предобработки данных до выбора лучшего решения. 
В Replay используется Spark, чтобы эффективно работать с большими датасетами.

RePlay поможет:
* Отфильтровать и разбить данные для обучения рекомендательной системы
* Обучить модель
* Подобрать гиперпараметры
* Оценить качество и сравнить модели
* Объединить рекомендации, полученные несколькими моделями

### Начало работы
Примеры использования библиотеки в директории `/experiments`.

### Алгоритмы, реализованные в RePlay
| Алгоритм       | Реализация          | Описание |
| ---------------|--------------|-------|
|Popular Recommender        |PySpark       | Рекомендует популярные объекты (встречавшиеся в истории взаимодействия чаще остальных)    |
|Popular By Users           |PySpark       | Рекомендует объекты, которые пользователь ранее выбирал чаще всего |
|Wilson Recommender         |Python CPU    | Рекомендует объекты по нижней границе доверительного интервала Вильсона для доли положительных оценок     |
|Random Recommender         |PySpark       | Рекомендует случайные объекты или сэмлпирует с вероятностью, пропорциональной популярности объекта   |
|K-Nearest Neighbours       |PySpark       | Рекомендует объекты, похожие на те, с которыми у пользователя было взаимодействие
|Classifier Recommender     |PySpark       | Алгоритм бинарной классификации для релевантности объекта для пользователя по их признакам          |
|Alternating Least Squares  |PySpark       | Алгоритм матричной факторизации [Collaborative Filtering for Implicit Feedback Datasets](https://ieeexplore.ieee.org/document/4781121)           |
|Neural Matrix Factorization|Python CPU/GPU| Алгоритм нейросетевой матричной факторизации на базе [Neural Collaborative Filtering](https://arxiv.org/pdf/1708.05031.pdf)          |
|SLIM                       |PySpark       | Алгоритм, обучающий матрицу близости объектов, для восстановления матрицы взаимодействия [SLIM: Sparse Linear Methods for Top-N Recommender Systems](http://glaros.dtc.umn.edu/gkhome/fetch/papers/SLIM2011icdm.pdf)          |
|ADMM SLIM                  |PySpark       | Улучшение стандартного алгоритма SLIM, [ADMM SLIM: Sparse Recommendations for Many Users](ADMM SLIM: Sparse Recommendations for Many Users)          |
|MultVAE                    |Python CPU/GPU| Вариационный автоэнкодер, восстанавливающий вектор взаимодействий для пользователя [Variational Autoencoders for Collaborative Filtering](Variational Autoencoders for Collaborative Filtering)          |
|Word2Vec Recommender       |Python CPU/GPU| Рекомендатель на основе word2vec, в котором объекты сопоставляются словам, а пользователи - предложениям.          |
|Обертка LightFM            |Python CPU    | Обертка для обучения моделей [LightFM](https://making.lyst.com/lightfm/docs/home.html)          |
|Обертка Implicit           |Python CPU    | Обертка для обучения моделей [Implicit](https://implicit.readthedocs.io/en/latest/)          |
|Stack Recommender          |Python CPU    | Модель стекинга, перевзвешивающая предсказания моделей первого уровня        |
|Двухуровневый классификатор|PySpark       | Классификатор, использующий для обучения эмбеддинги пользователей и объектов, полученные базовым алгоритмом (например, матричной факторизацией), и признаки пользователей и объектов, переданные пользователем.   |

Выбор алгоритма рекомендательной системы зависит от данных и требований пользователя к рекомендациям.

**Особенности данных и алгоритмы**
Чтобы выбрать алгоритм, нужно понять, к какому типу относятся данные для обучения, и насколько изменчив состав пользователей и объектов.  
- _Тип входных данных._ В качестве входных данных модели используют историю взаимодействия пользователей и объектов (коллаборативная информация) и информацию о признаках пользователей, объектов и контектста.
Использование признаковых описаний может улучшить качество рекомендаций по сравнению с решениями, использующими только историю взаимодействия, а также помочь с "холодным стартом" (рекомендациями для пользователей и объектов, отсутствующих в истории взаимодействия).
По типу входных данных алгоритмы в RePlay делятся на:
    - Collaborative, коллаборативные. Используют историю взаимодействия пользователей и объектов для построения рекомендаций. 
    - Content-based. Используют признаковые описания пользователей и объектов для построения рекомендаций.
    - Hybrid, гибридные. Используют коллаборативную информацию, признаки пользователей/объектов, результаты работы других алгоритмов.
- _Тип взаимодействия._ История взаимодействия может отражать явные предпочтения пользователя, например, оценки, покупки (explicit feedback) или неявные предпочтения, например, время просмотра (implicit feedback). 
    Implicit feedback можно привести к explicit, придумав для этого правила. 
    Но некоторые алгоритмы изначально ориентированы на работу с implicit feedback и позволяют работать с данными как есть. 
- _Постоянство пользователей._ Некоторые алгоритмы требуют переобучения модели, чтобы рекомендовать пользователям, отсутствующим в обучающей выборке.
- _Постоянство объектов._ Большинство алгоритмы требуют переобучения модели, чтобы рекомендовать объекты, отсутствующие в обучающей выборке.

| Алгоритм       | Тип данных          | Подходит для implicit | Рекомендует для новых пользователи | Рекомендует новые объекты |
| ---------------|--------------|-------|-------|-------|
|Popular Recommender        |Collaborative    | -          | + | - |
|Popular By Users           |Collaborative    | -          | - | - |
|Wilson Recommender         |Collaborative    | -          | + | - |
|Random Recommender         |Collaborative    | -          | + | - |
|K-Nearest Neighbours       |Collaborative    | -          | + | - |
|Classifier Recommender     |Content-based    | -          | + | + |
|Alternating Least Squares  |Collaborative    | +          | - | - |
|Neural Matrix Factorization|Collaborative    | +          | - | - |
|SLIM                       |Collaborative    | -          | - | - |
|ADMM SLIM                  |Collaborative    | -          | - | - |
|Mult-VAE                   |Collaborative    | -          | + | - |
|Word2Vec Recommender       |Collaborative    | -          | + | - |
|Обертка LightFM            |Hybrid           | +          | + | + |
|Обертка Implicit           |Collaborative    | +          | - | - |
|Stack Recommender          | `*`             | `*`        | `*` | `*` |
|Двухуровневый классификатор|Hybrid           | -          | `*` | `*` |

`*` - зависит от алгоритмов, используемых в качестве базовых. 

**Требования к рекомендациям и алгоритмы**
Перед выбором алгоритма стоит оценить, какие рекомендации мы ожидаем получить. 
* _Персонализированность рекомендаций._ Иногда достаточно рекомендовать новые и популярные объекты всем пользователям, но чаще рекомендации должны быть персоналазированными, то есть определяться профилем пользователя и его историей.  
* _Рекомендации для холодных пользователей_ (пользователи, которые не взаимодействовали с объектами)
* _Рекомендации для холодных объектов_ (объекты, для которых отсутствует история взаимодействия с пользователями)
* _Рекомендации новых для пользователя объектов._ Иногда достаточно порекомендовать пользователю какие-то объекты из его же истории взаимодействия. Хороший бейзлайн - рекомендации самого популярного из истории пользователя, но в классическом подходе от рекомендательной системы требуется рекомендация объектов, с которыми пользователь еще не взаимодействовал.

| Алгоритм       | Персонализированные | Холодные пользователи | Холодные объекты |  Новые объекты для пользователя |
| ---------------|--------------|-------|-------|-------|
|Popular Recommender          | - | + | - | + |
|Popular By Users             | + | - | - | - |
|Wilson Recommender           | - | + | - | + |
|Random Recommender           | - | + | - | + |
|K-Nearest Neighbours         | + | + | - | + |
|Classifier Recommender       | + | + | + | + |
|Alternating Least Squares    | + | - | - | + |
|Neural Matrix Factorization  | + | - | - | + |
|SLIM                         | + | - | - | + |
|ADMM SLIM                    | + | - | - | + |
|Mult-VAE                     | + | - | - | + |
|Word2Vec Recommender         | + | - | - | + |
|Обертка LightFM              | + | + | + | + |
|Обертка Implicit             | + | - | - | + |
|Stack Recommender            | + | `*` | `*` | `*` |
|Двухуровневый классификатор  | + | `*` | `*` | `*` |

`*` - зависит от алгоритмов, используемых в качестве базовых.

Больше информации об алгоритмах - в документации к RePlay.

### Метрики
В библиотеке реализованы метрики для оценки качества рекомендательных систем: HitRate, Precision, MAP, Recall, ROC-AUC, MRR, NDCG, Surprisal, Unexpectedness, Coverage.
Метрики можно посчитать для различных значений _k_ (числа рекомендаций для подсчета метрики), оценить среднее или медианное значение метрики по пользователям и нижнюю границу доверительного интервала.  

### Сценарии
В библиотеке реализованы сценарии для обучения модели с нуля, включая:
* разбиение данных на обучающую и валидационную выборки
* автоматический подбор гиперпараметров моделей
* расчёт метрик и сравнение моделей
* обучение на всём объёме данных и построение рекомендаций

### Эксперименты
Класс Experiment позволяет посчитать метрики для рекомендаций, полученных несколькими моделями, и сравнить их. 

## Как начать пользоваться библиотекой

### Установка
Для корректной работы необходимы python 3.6+ и java 8+. \

Клонируйте репозиторий RePlay: \
 в _sigma_:
```bash
git clone https://sbtatlas.sigma.sbrf.ru/stash/scm/ailab/replay.git
```
в _alpha_:
```bash
git clone ssh://git@stash.delta.sbrf.ru:7999/ailabrecsys/replay.git
```
 и установите библиотеку с помощью poetry:
```
cd replay
pip install --upgrade pip
pip install poetry
poetry install
```

### Проверка работы библиотеки
Запустите тесты для проверки корректности установки. \
Из директории `replay`:
```bash
pytest ./tests
```

### Документация

Чтобы сформировать документацию, выполните из директории `replay`:
```bash
cd ./docs
mkdir -p _static
make clean html
```
Документация будет доступна в `replay/docs/_build/html/index.html`

## Как присоединиться к разработке
[Инструкция для разработчика](README_dev.md)
