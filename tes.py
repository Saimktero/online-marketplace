"""Значения в качестве свойств для компонента Pagination"""

1) totalCount: общее количество данных, доступных из источника.

2) currentPage: текущая активная страница. Мы будем использовать индекс, начинающийся с 1 вместо традиционного индекса,
начинающегося с 0, для нашего currentPage значения.

3) pageSize: максимальное количество данных, отображаемое на одной странице.

4) onPageChange: функция обратного вызова, которая вызывается с обновлённым значением страницы при её смене.

5) siblingCount (необязательно): минимальное количество кнопок перехода на следующую страницу, которые будут
отображаться с каждой стороны от текущей кнопки перехода на страницу. По умолчанию 1.

6) className (необязательно): класс, который нужно добавить к контейнеру верхнего уровня.



./src/usePagination.js
import math

export const usePagination = ({
    totalCount,
    pageSize,
    siblingCount = 1,
    currentPage
}) => {
    const paginationRange = useMemo(() => {
    const totalPageCount = math.ceil(totalCount / pageSize);

    // Количество страниц определяется как siblingCount + Первая страница + Последняя страница + Текущая страница + 2*ТОЧКИ
    const totalPageNumbers = siblingCount + 5;








    const range = (start, end) => {
        let length = end - start + 1;



        return Array.from({ length }, (_, idx) => idx + start);
};







    }, [totalCount, pageSize, siblingCount, currentPage]);
    return paginationRange;
}
