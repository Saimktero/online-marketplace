function Pagination({ nextPage, prevPage, loadPage }) {
  return (
    <div>
      {prevPage ? <button onClick={() => loadPage(prevPage)}>Назад</button> : <button disabled>Назад</button>}
      {nextPage ? <button onClick={() => loadPage(nextPage)}>Вперёд</button> : <button disabled>Вперёд</button>}
    </div>
  );
}

export default Pagination;